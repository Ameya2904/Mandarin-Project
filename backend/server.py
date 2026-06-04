"""Mandarin Learning App - FastAPI Backend
Provides authentication, spaced repetition flashcards, lessons, drills, and speaking practice.
"""
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import uuid
import bcrypt
import jwt
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta, timezone

from seed_data import NPCR_LESSONS, SENTENCE_DRILLS
from openai import AsyncOpenAI
import tempfile
import json
import asyncio
import base64 as b64lib
import io
import numpy as np
from PIL import Image
import easyocr
from pypinyin import lazy_pinyin, Style
import re
import nltk

# Ensure WordNet corpus is available for synonym checking
try:
    from nltk.corpus import wordnet as wn
    wn.synsets('call')  # probe to trigger LookupError if data missing
except LookupError:
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    from nltk.corpus import wordnet as wn

# ---------- Setup ----------
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

JWT_SECRET = os.environ['JWT_SECRET_KEY']
JWT_ALGO = os.environ.get('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 43200))
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

app = FastAPI(title="Mandarin Learning API")
api_router = APIRouter(prefix="/api")
security = HTTPBearer(auto_error=False)

# Stage intervals in days for spaced repetition
SRS_INTERVALS = {1: 1, 2: 2, 3: 7, 4: 30, 5: 90, 6: 365}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Lazy-initialized EasyOCR reader (loads ~100MB models on first use)
_ocr_reader: easyocr.Reader | None = None

def _get_ocr_reader() -> easyocr.Reader:
    global _ocr_reader
    if _ocr_reader is None:
        logger.info("Initializing EasyOCR reader (first use)...")
        _ocr_reader = easyocr.Reader(['ch_sim'], gpu=False)
    return _ocr_reader


# ---------- Pydantic Models ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=1)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: str
    email: str
    name: str
    daily_goal: int = 20
    streak_count: int = 0
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class CustomVocabCreate(BaseModel):
    simplified: str = Field(min_length=1)
    pinyin: str = Field(min_length=1)
    english: str = Field(min_length=1)
    example_chinese: Optional[str] = ""
    example_pinyin: Optional[str] = ""
    example_english: Optional[str] = ""
    part_of_speech: Optional[str] = "custom"


class DeckAddRequest(BaseModel):
    vocabulary_ids: List[str]


class WritingRecognizeRequest(BaseModel):
    image_base64: str
    target_chinese: str
    vocabulary_id: Optional[str] = None


class FlashcardReviewRequest(BaseModel):
    vocabulary_id: str
    was_correct: bool
    response_time_ms: Optional[int] = None
    mode: Optional[str] = "reading"  # reading | writing | speaking
    skip_srs: bool = False  # log history only, don't advance SRS stage


class DrillAttemptRequest(BaseModel):
    drill_id: str
    user_answer: str
    was_correct: bool
    response_time_ms: Optional[int] = None


class SemanticMatchRequest(BaseModel):
    answer: str
    target: str


class SpeakingAttemptRequest(BaseModel):
    target_chinese: str
    spoken_text: str
    vocabulary_id: Optional[str] = None


class UserSettingsUpdate(BaseModel):
    name: Optional[str] = None
    daily_goal: Optional[int] = None
    learner_level: Optional[str] = None


# ---------- Auth Helpers ----------
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


async def get_current_user(creds: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> dict:
    if creds is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALGO])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await db.users.find_one({"id": user_id}, {"_id": 0, "hashed_password": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def user_to_public(doc: dict) -> UserPublic:
    return UserPublic(
        id=doc["id"],
        email=doc["email"],
        name=doc["name"],
        daily_goal=doc.get("daily_goal", 20),
        streak_count=doc.get("streak_count", 0),
        created_at=doc["created_at"],
    )


# ---------- Seed Data on Startup ----------
async def seed_lessons_and_vocab():
    existing = await db.lessons.count_documents({})
    if existing == len(NPCR_LESSONS):
        logger.info(f"Lessons already seeded ({existing}). Skipping.")
        return

    if existing != len(NPCR_LESSONS) and existing > 0:
        logger.info(f"Lesson count changed ({existing} -> {len(NPCR_LESSONS)}). Reseeding lessons/vocab/drills (user data preserved).")
        await db.lessons.delete_many({})
        await db.vocabulary.delete_many({})
        await db.drills.delete_many({})

    logger.info("Seeding NPCR lessons and vocabulary...")
    for lesson in NPCR_LESSONS:
        lesson_id = str(uuid.uuid4())
        vocab_ids = []
        for vocab in lesson["vocabulary"]:
            vocab_id = str(uuid.uuid4())
            await db.vocabulary.insert_one({
                "id": vocab_id,
                "lesson_id": lesson_id,
                "lesson_number": lesson["lesson_number"],
                **vocab
            })
            vocab_ids.append(vocab_id)

        await db.lessons.insert_one({
            "id": lesson_id,
            "lesson_number": lesson["lesson_number"],
            "title": lesson["title"],
            "subtitle": lesson["subtitle"],
            "description": lesson["description"],
            "level": lesson["level"],
            "video_url": lesson["video_url"],
            "dialogue": lesson["dialogue"],
            "grammar_notes": lesson["grammar_notes"],
            "vocabulary_ids": vocab_ids,
            "vocabulary_count": len(vocab_ids),
        })

    for drill in SENTENCE_DRILLS:
        await db.drills.insert_one({"id": str(uuid.uuid4()), **drill})

    logger.info(f"Seeded {len(NPCR_LESSONS)} lessons, vocabulary, and {len(SENTENCE_DRILLS)} drills.")


@app.on_event("startup")
async def startup():
    await db.users.create_index("email", unique=True)
    await db.flashcards.create_index([("user_id", 1), ("vocabulary_id", 1)], unique=True)
    await db.flashcards.create_index([("user_id", 1), ("next_review_at", 1)])
    await db.user_deck.create_index([("user_id", 1), ("vocabulary_id", 1)], unique=True)
    await db.vocabulary.create_index("created_by")
    await seed_lessons_and_vocab()
    await migrate_legacy_decks()


async def migrate_legacy_decks():
    """Back-fill user_deck for users who already have flashcards but no deck entries."""
    pipeline = [
        {"$group": {"_id": "$user_id", "vocab_ids": {"$addToSet": "$vocabulary_id"}}},
    ]
    cursor = db.flashcards.aggregate(pipeline)
    total = 0
    async for row in cursor:
        user_id = row["_id"]
        vocab_ids = row["vocab_ids"]
        for vid in vocab_ids:
            existing = await db.user_deck.find_one({"user_id": user_id, "vocabulary_id": vid})
            if not existing:
                await db.user_deck.insert_one({
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "vocabulary_id": vid,
                    "added_at": datetime.now(timezone.utc),
                })
                total += 1
    if total:
        logger.info(f"Migrated {total} legacy deck entries from existing flashcards.")


@app.on_event("shutdown")
async def shutdown():
    client.close()


# ---------- Auth Endpoints ----------
@api_router.post("/auth/signup", response_model=TokenResponse)
async def signup(payload: UserCreate):
    email = payload.email.lower()
    existing = await db.users.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    user_doc = {
        "id": user_id,
        "email": email,
        "name": payload.name,
        "hashed_password": hash_password(payload.password),
        "daily_goal": 20,
        "streak_count": 0,
        "learner_level": "Beginner",
        "last_active_date": now.date().isoformat(),
        "created_at": now,
    }
    await db.users.insert_one(user_doc)

    token = create_access_token(user_id)
    return TokenResponse(access_token=token, user=user_to_public(user_doc))


@api_router.post("/auth/login", response_model=TokenResponse)
async def login(payload: UserLogin):
    email = payload.email.lower()
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Update streak
    today = datetime.now(timezone.utc).date()
    last_active = user.get("last_active_date")
    new_streak = user.get("streak_count", 0)
    if last_active:
        last_date = datetime.fromisoformat(last_active).date()
        if last_date == today:
            pass  # same day, keep streak
        elif (today - last_date).days == 1:
            new_streak += 1
        else:
            new_streak = 1
    else:
        new_streak = 1

    await db.users.update_one(
        {"id": user["id"]},
        {"$set": {"last_active_date": today.isoformat(), "streak_count": new_streak}}
    )
    user["streak_count"] = new_streak

    token = create_access_token(user["id"])
    return TokenResponse(access_token=token, user=user_to_public(user))


@api_router.get("/auth/me", response_model=UserPublic)
async def get_me(current_user: dict = Depends(get_current_user)):
    return user_to_public(current_user)


@api_router.put("/auth/me", response_model=UserPublic)
async def update_me(payload: UserSettingsUpdate, current_user: dict = Depends(get_current_user)):
    updates = {k: v for k, v in payload.dict().items() if v is not None}
    if updates:
        await db.users.update_one({"id": current_user["id"]}, {"$set": updates})
    refreshed = await db.users.find_one({"id": current_user["id"]}, {"_id": 0, "hashed_password": 0})
    return user_to_public(refreshed)


# ---------- Lesson Endpoints ----------
@api_router.get("/lessons")
async def list_lessons(current_user: dict = Depends(get_current_user)):
    lessons = await db.lessons.find({}, {"_id": 0}).sort("lesson_number", 1).to_list(100)
    # Add progress info per lesson
    for lesson in lessons:
        vocab_ids = lesson.get("vocabulary_ids", [])
        if vocab_ids:
            mastered = await db.flashcards.count_documents({
                "user_id": current_user["id"],
                "vocabulary_id": {"$in": vocab_ids},
                "current_stage": {"$gte": 4}
            })
            started = await db.flashcards.count_documents({
                "user_id": current_user["id"],
                "vocabulary_id": {"$in": vocab_ids},
            })
            lesson["progress"] = {"mastered": mastered, "started": started, "total": len(vocab_ids)}
        else:
            lesson["progress"] = {"mastered": 0, "started": 0, "total": 0}
    return lessons


@api_router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: str, current_user: dict = Depends(get_current_user)):
    lesson = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    vocab = await db.vocabulary.find(
        {"lesson_id": lesson_id}, {"_id": 0}
    ).to_list(100)
    # Mark which vocab is in user's deck
    deck_entries = await db.user_deck.find({"user_id": current_user["id"]}, {"vocabulary_id": 1, "_id": 0}).to_list(10000)
    deck_set = {e["vocabulary_id"] for e in deck_entries}
    for v in vocab:
        v["in_deck"] = v["id"] in deck_set
    lesson["vocabulary"] = vocab
    return lesson


# ---------- Flashcard / SRS Endpoints ----------
@api_router.get("/flashcards/due")
async def get_due_flashcards(limit: int = 20, current_user: dict = Depends(get_current_user)):
    """Get cards due for review today (or earlier)."""
    now = datetime.now(timezone.utc)
    cards = await db.flashcards.find(
        {"user_id": current_user["id"], "next_review_at": {"$lte": now}},
        {"_id": 0}
    ).sort("next_review_at", 1).limit(limit).to_list(limit)

    # Enrich with vocabulary
    result = []
    for card in cards:
        vocab = await db.vocabulary.find_one({"id": card["vocabulary_id"]}, {"_id": 0})
        if vocab:
            result.append({**card, "vocabulary": vocab})
    return result


@api_router.get("/flashcards/new")
async def get_new_flashcards(lesson_id: Optional[str] = None, limit: int = 10, current_user: dict = Depends(get_current_user)):
    """Get vocabulary words the user has added to deck but never reviewed yet."""
    user_id = current_user["id"]

    # Vocabulary IDs in the user's deck
    deck_entries = await db.user_deck.find({"user_id": user_id}, {"vocabulary_id": 1, "_id": 0}).to_list(10000)
    deck_ids = [e["vocabulary_id"] for e in deck_entries]
    if not deck_ids:
        return []

    # Vocabulary IDs the user has already reviewed (has a flashcard)
    existing = await db.flashcards.find({"user_id": user_id}, {"vocabulary_id": 1, "_id": 0}).to_list(10000)
    existing_ids = {e["vocabulary_id"] for e in existing}

    new_ids = [vid for vid in deck_ids if vid not in existing_ids]
    if not new_ids:
        return []

    query: dict = {"id": {"$in": new_ids}}
    if lesson_id:
        query["lesson_id"] = lesson_id

    vocab_list = await db.vocabulary.find(query, {"_id": 0}).sort("lesson_number", 1).limit(limit).to_list(limit)
    return vocab_list


@api_router.get("/flashcards/schedule")
async def get_review_schedule(days: int = 14, current_user: dict = Depends(get_current_user)):
    """Return how many cards are due on each upcoming day (next `days` days)."""
    user_id = current_user["id"]
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)

    cards = await db.flashcards.find(
        {"user_id": user_id, "next_review_at": {"$gte": now, "$lte": end}},
        {"_id": 0, "next_review_at": 1},
    ).to_list(5000)

    from collections import defaultdict
    counts: dict = defaultdict(int)
    for card in cards:
        date_key = card["next_review_at"].strftime("%Y-%m-%d")
        counts[date_key] += 1

    schedule = []
    for i in range(days):
        date = (now + timedelta(days=i + 1)).date()
        date_key = date.strftime("%Y-%m-%d")
        if date_key in counts:
            schedule.append({"date": date_key, "count": counts[date_key]})

    return schedule


# ---------- Semantic matching helpers ----------

def _normalize_en(s: str) -> str:
    s = (s or '').strip().lower()
    s = re.sub(r'[.;]+$', '', s)
    s = re.sub(r'^(to |a |an |the )', '', s)
    return s.strip()


def _word_synonyms(word: str) -> set:
    synonyms = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name().lower().replace('_', ' '))
    return synonyms


def _semantic_words_match(w1: str, w2: str) -> bool:
    if w1 == w2:
        return True
    syns1 = _word_synonyms(w1)
    syns2 = _word_synonyms(w2)
    return w2 in syns1 or w1 in syns2


@api_router.post("/vocabulary/semantic-match")
async def check_semantic_match(payload: SemanticMatchRequest, current_user: dict = Depends(get_current_user)):
    answer_clean = _normalize_en(payload.answer)
    parts = re.split(r'[;,/]|\bor\b', payload.target)
    target_parts = [_normalize_en(p) for p in parts if p.strip()]

    for part in target_parts:
        if _semantic_words_match(answer_clean, part):
            return {"match": True}

    return {"match": False}


@api_router.post("/flashcards/review")
async def submit_review(payload: FlashcardReviewRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    now = datetime.now(timezone.utc)

    vocab = await db.vocabulary.find_one({"id": payload.vocabulary_id})
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")

    existing = await db.flashcards.find_one({"user_id": user_id, "vocabulary_id": payload.vocabulary_id})

    if payload.skip_srs:
        # Log to review history only — don't touch SRS stage
        card_id = existing["id"] if existing else None
        if card_id:
            await db.review_history.insert_one({
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "vocabulary_id": payload.vocabulary_id,
                "flashcard_id": card_id,
                "was_correct": payload.was_correct,
                "response_time_ms": payload.response_time_ms,
                "mode": payload.mode or "reading",
                "timestamp": now,
            })
        current_stage = existing["current_stage"] if existing else None
        next_review = existing["next_review_at"] if existing else None
        return {
            "success": True,
            "new_stage": current_stage,
            "next_review_at": next_review.isoformat() if next_review else None,
        }

    if existing:
        if payload.was_correct:
            new_stage = min(existing["current_stage"] + 1, 6)
            correct_count = existing.get("correct_count", 0) + 1
            incorrect_count = existing.get("incorrect_count", 0)
        else:
            new_stage = 1
            correct_count = existing.get("correct_count", 0)
            incorrect_count = existing.get("incorrect_count", 0) + 1

        next_review = now + timedelta(days=SRS_INTERVALS[new_stage])
        await db.flashcards.update_one(
            {"user_id": user_id, "vocabulary_id": payload.vocabulary_id},
            {"$set": {
                "current_stage": new_stage,
                "next_review_at": next_review,
                "correct_count": correct_count,
                "incorrect_count": incorrect_count,
                "last_reviewed_at": now,
            }}
        )
        card_id = existing["id"]
    else:
        # New card
        new_stage = 2 if payload.was_correct else 1
        next_review = now + timedelta(days=SRS_INTERVALS[new_stage])
        card_id = str(uuid.uuid4())
        await db.flashcards.insert_one({
            "id": card_id,
            "user_id": user_id,
            "vocabulary_id": payload.vocabulary_id,
            "current_stage": new_stage,
            "next_review_at": next_review,
            "correct_count": 1 if payload.was_correct else 0,
            "incorrect_count": 0 if payload.was_correct else 1,
            "last_reviewed_at": now,
            "created_at": now,
        })

    # Log review history
    await db.review_history.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "vocabulary_id": payload.vocabulary_id,
        "flashcard_id": card_id,
        "was_correct": payload.was_correct,
        "response_time_ms": payload.response_time_ms,
        "mode": payload.mode or "reading",
        "timestamp": now,
    })

    return {"success": True, "new_stage": new_stage, "next_review_at": next_review.isoformat()}


# ---------- Drill Endpoints ----------
@api_router.get("/drills")
async def list_drills(
    lesson_number: Optional[int] = None,
    part: Optional[int] = None,
    limit: int = 500,
    current_user: dict = Depends(get_current_user),
):
    import random
    query = {}
    if lesson_number is not None:
        query["lesson_number"] = lesson_number
    if part is not None:
        query["part"] = part
    drills = await db.drills.find(query, {"_id": 0}).to_list(2000)

    expanded = []
    for d in drills:
        n = max(1, int(d.get("repeat_count", 1)))
        for _ in range(n):
            expanded.append(d)
    random.shuffle(expanded)
    return expanded[:limit]


@api_router.post("/drills/attempt")
async def submit_drill_attempt(payload: DrillAttemptRequest, current_user: dict = Depends(get_current_user)):
    await db.drill_attempts.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": current_user["id"],
        "drill_id": payload.drill_id,
        "user_answer": payload.user_answer,
        "was_correct": payload.was_correct,
        "response_time_ms": payload.response_time_ms,
        "timestamp": datetime.now(timezone.utc),
    })
    return {"success": True}


# ---------- Speaking / Pronunciation ----------
def normalize_chinese(text: str) -> str:
    """Strip whitespace, punctuation for comparison."""
    import re
    return re.sub(r'[\s\W_，。!?,.!?]', '', text or '')


def pinyin_syllables(text: str) -> list[str]:
    """Tone-numbered pinyin syllables, e.g. '你好' -> ['ni3', 'hao3']."""
    return [s.lower() for s in lazy_pinyin(text, style=Style.TONE3)]


def _strip_tone(syllable: str) -> str:
    """Drop the trailing tone digit from a TONE3 syllable ('hao3' -> 'hao')."""
    return syllable.rstrip("012345")


def pinyin_display(text: str) -> str:
    """Space-separated pinyin with tone marks, for showing back to the learner."""
    return " ".join(lazy_pinyin(text, style=Style.TONE))


def score_pronunciation(target: str, spoken: str) -> dict:
    """Score spoken pinyin against the target at the syllable level.

    Full credit for a syllable whose sound *and* tone match the target; half
    credit when the syllable (sound) is right but the tone is wrong. This is
    order-independent (a bag/multiset match) so a single dropped or swapped
    syllable doesn't cascade into everything after it counting as wrong.
    """
    from collections import Counter

    target_syls = pinyin_syllables(target)
    spoken_syls = pinyin_syllables(spoken)
    total = len(target_syls)
    if total == 0:
        return {"score": 0, "correct": False, "syllables_right": 0,
                "tones_wrong": 0, "total": 0}

    pool = Counter(spoken_syls)

    # Pass 1: exact syllable + tone match.
    full = 0
    unmatched: list[str] = []
    for syl in target_syls:
        if pool.get(syl, 0) > 0:
            pool[syl] -= 1
            full += 1
        else:
            unmatched.append(syl)

    # Pass 2: same base sound but wrong tone -> partial credit.
    base_pool: Counter = Counter()
    for syl, cnt in pool.items():
        if cnt > 0:
            base_pool[_strip_tone(syl)] += cnt
    tone_wrong = 0
    for syl in unmatched:
        base = _strip_tone(syl)
        if base_pool.get(base, 0) > 0:
            base_pool[base] -= 1
            tone_wrong += 1

    credit = full + 0.5 * tone_wrong
    score = round(credit / total * 100)
    correct = full == total and len(spoken_syls) == total
    return {
        "score": score,
        "correct": correct,
        "syllables_right": full + tone_wrong,
        "tones_wrong": tone_wrong,
        "total": total,
    }


def _pronunciation_feedback(p: dict) -> str:
    """Human feedback string for a score_pronunciation result."""
    if p["correct"]:
        return "Perfect pronunciation! 完美!"
    if p["total"] and p["syllables_right"] == p["total"] and p["tones_wrong"] > 0:
        return "All the right sounds — but check your tones! 🎵"
    if p["tones_wrong"] > 0:
        return "Some sounds are right, but watch your tones."
    if p["score"] >= 80:
        return "Great pronunciation! Almost there."
    if p["score"] >= 50:
        return "Good attempt. Some syllables were off."
    return "Try again. Listen and speak more clearly."


@api_router.post("/speaking/evaluate")
async def evaluate_speaking(payload: SpeakingAttemptRequest, current_user: dict = Depends(get_current_user)):
    """Compare spoken text against target sentence."""
    target_normalized = normalize_chinese(payload.target_chinese)
    spoken_normalized = normalize_chinese(payload.spoken_text)

    if not spoken_normalized:
        return {"correct": False, "score": 0, "feedback": "No speech detected. Try again.", "spoken_text": payload.spoken_text}

    # Syllable-level pinyin scoring with partial credit for tone errors.
    p = score_pronunciation(target_normalized, spoken_normalized)
    score = p["score"]
    exact_match = p["correct"]
    feedback = _pronunciation_feedback(p)

    await db.speaking_attempts.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": current_user["id"],
        "target_chinese": payload.target_chinese,
        "spoken_text": payload.spoken_text,
        "score": score,
        "exact_match": exact_match,
        "vocabulary_id": payload.vocabulary_id,
        "timestamp": datetime.now(timezone.utc),
    })

    return {
        "correct": exact_match,
        "score": score,
        "feedback": feedback,
        "spoken_text": payload.spoken_text,
        "target_text": payload.target_chinese,
        "target_pinyin": pinyin_display(target_normalized),
        "spoken_pinyin": pinyin_display(spoken_normalized),
        "tones_wrong": p["tones_wrong"],
        "syllables_right": p["syllables_right"],
        "syllable_count": p["total"],
    }


# ---------- Progress / Dashboard ----------
@api_router.get("/progress/dashboard")
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    now = datetime.now(timezone.utc)
    today_start = datetime.combine(now.date(), datetime.min.time()).replace(tzinfo=timezone.utc)

    due_count = await db.flashcards.count_documents({"user_id": user_id, "next_review_at": {"$lte": now}})
    total_cards = await db.flashcards.count_documents({"user_id": user_id})
    mastered = await db.flashcards.count_documents({"user_id": user_id, "current_stage": {"$gte": 4}})

    reviews_today = await db.review_history.count_documents({"user_id": user_id, "timestamp": {"$gte": today_start}})
    correct_today = await db.review_history.count_documents({"user_id": user_id, "timestamp": {"$gte": today_start}, "was_correct": True})

    # Total available new cards
    new_count = await db.vocabulary.count_documents({}) - total_cards

    daily_goal = current_user.get("daily_goal", 20)

    return {
        "due_count": due_count,
        "new_count": max(new_count, 0),
        "total_cards": total_cards,
        "mastered_count": mastered,
        "reviews_today": reviews_today,
        "correct_today": correct_today,
        "daily_goal": daily_goal,
        "streak_count": current_user.get("streak_count", 0),
        "progress_percent": min(round((reviews_today / max(daily_goal, 1)) * 100), 100),
    }


@api_router.get("/progress/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]

    total_reviews = await db.review_history.count_documents({"user_id": user_id})
    correct_reviews = await db.review_history.count_documents({"user_id": user_id, "was_correct": True})
    retention = round((correct_reviews / total_reviews) * 100) if total_reviews > 0 else 0

    mastered = await db.flashcards.count_documents({"user_id": user_id, "current_stage": {"$gte": 4}})
    learning = await db.flashcards.count_documents({"user_id": user_id, "current_stage": {"$lt": 4}})

    # Weak words: incorrect_count > correct_count and at least 2 attempts
    weak_cards = await db.flashcards.find(
        {"user_id": user_id, "$expr": {"$gt": ["$incorrect_count", "$correct_count"]}},
        {"_id": 0}
    ).limit(10).to_list(10)
    weak_words = []
    for card in weak_cards:
        vocab = await db.vocabulary.find_one({"id": card["vocabulary_id"]}, {"_id": 0})
        if vocab:
            weak_words.append({
                "simplified": vocab["simplified"],
                "pinyin": vocab["pinyin"],
                "english": vocab["english"],
                "correct": card.get("correct_count", 0),
                "incorrect": card.get("incorrect_count", 0),
            })

    # Speaking stats
    speaking_attempts = await db.speaking_attempts.count_documents({"user_id": user_id})

    return {
        "total_reviews": total_reviews,
        "correct_reviews": correct_reviews,
        "retention_rate": retention,
        "mastered_count": mastered,
        "learning_count": learning,
        "weak_words": weak_words,
        "speaking_attempts": speaking_attempts,
        "streak_count": current_user.get("streak_count", 0),
    }


# ---------- Whisper Transcription ----------
@api_router.post("/speaking/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    target_chinese: str = "",
    vocabulary_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
):
    """Accept an audio file (m4a/wav/webm), transcribe via OpenAI Whisper-1 (zh),
    then compare to target_chinese (if provided) for pronunciation feedback."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured on server")

    filename = file.filename or "audio.m4a"
    suffix = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ".m4a"
    if suffix.lstrip(".") not in {"mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"}:
        suffix = ".m4a"

    contents = await file.read()
    if len(contents) > 25 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Audio file too large (max 25MB)")
    if len(contents) < 100:
        raise HTTPException(status_code=400, detail="Audio file too small / empty")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(contents)
    tmp.close()

    try:
        oai = AsyncOpenAI(api_key=OPENAI_API_KEY)
        with open(tmp.name, "rb") as f:
            transcribed = await oai.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="zh",
                response_format="text",
                prompt="普通话，简体中文。",
            )
        if not isinstance(transcribed, str):
            transcribed = getattr(transcribed, "text", "") or str(transcribed)
    except Exception as e:
        logger.exception("Whisper transcription failed")
        raise HTTPException(status_code=502, detail=f"Transcription failed: {str(e)}")
    finally:
        try:
            os.remove(tmp.name)
        except OSError:
            pass

    transcribed = (transcribed or "").strip()

    # If a target was provided, compute comparison
    result = {"transcribed_text": transcribed}
    if target_chinese:
        target_norm = normalize_chinese(target_chinese)
        spoken_norm = normalize_chinese(transcribed)

        # Syllable-level pinyin scoring: full credit when sound + tone match,
        # half credit when the syllable is right but the tone is wrong. This
        # also handles homophones (same pinyin, different characters).
        p = score_pronunciation(target_norm, spoken_norm)
        score = p["score"]
        exact_match = p["correct"]
        feedback = _pronunciation_feedback(p)
        target_pinyin = pinyin_display(target_norm)
        spoken_pinyin = pinyin_display(spoken_norm) if spoken_norm else ""

        await db.speaking_attempts.insert_one({
            "id": str(uuid.uuid4()),
            "user_id": current_user["id"],
            "target_chinese": target_chinese,
            "spoken_text": transcribed,
            "score": score,
            "exact_match": exact_match,
            "vocabulary_id": vocabulary_id,
            "source": "whisper",
            "timestamp": datetime.now(timezone.utc),
        })

        result.update({
            "correct": exact_match,
            "score": score,
            "feedback": feedback,
            "target_text": target_chinese,
            "target_pinyin": target_pinyin,
            "spoken_pinyin": spoken_pinyin,
            "tones_wrong": p["tones_wrong"],
            "syllables_right": p["syllables_right"],
            "syllable_count": p["total"],
        })

    return result


# ---------- Deck Management ----------
@api_router.get("/deck")
async def list_deck(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    deck = await db.user_deck.find({"user_id": user_id}, {"_id": 0}).sort("added_at", -1).to_list(10000)
    # Enrich with vocabulary
    result = []
    for entry in deck:
        vocab = await db.vocabulary.find_one({"id": entry["vocabulary_id"]}, {"_id": 0})
        if vocab:
            # Find flashcard if exists
            card = await db.flashcards.find_one({"user_id": user_id, "vocabulary_id": entry["vocabulary_id"]}, {"_id": 0})
            result.append({
                **entry,
                "vocabulary": vocab,
                "current_stage": card.get("current_stage") if card else None,
                "next_review_at": card.get("next_review_at").isoformat() if card and card.get("next_review_at") else None,
            })
    return result


@api_router.post("/deck/add")
async def add_to_deck(payload: DeckAddRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    now = datetime.now(timezone.utc)
    added = 0
    for vid in payload.vocabulary_ids:
        vocab = await db.vocabulary.find_one({"id": vid})
        if not vocab:
            continue
        existing = await db.user_deck.find_one({"user_id": user_id, "vocabulary_id": vid})
        if existing:
            continue
        await db.user_deck.insert_one({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "vocabulary_id": vid,
            "added_at": now,
        })
        added += 1
    return {"added": added}


@api_router.delete("/deck/{vocabulary_id}")
async def remove_from_deck(vocabulary_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    deck_res = await db.user_deck.delete_one({"user_id": user_id, "vocabulary_id": vocabulary_id})
    # Also remove their flashcard for this word
    await db.flashcards.delete_one({"user_id": user_id, "vocabulary_id": vocabulary_id})
    return {"removed": deck_res.deleted_count > 0}


# ---------- Custom Vocabulary ----------
@api_router.post("/vocabulary/custom")
async def create_custom_vocab(payload: CustomVocabCreate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    now = datetime.now(timezone.utc)
    vocab_id = str(uuid.uuid4())
    doc = {
        "id": vocab_id,
        "lesson_id": None,
        "lesson_number": None,
        "simplified": payload.simplified.strip(),
        "traditional": payload.simplified.strip(),
        "pinyin": payload.pinyin.strip(),
        "english": payload.english.strip(),
        "part_of_speech": payload.part_of_speech or "custom",
        "example_chinese": (payload.example_chinese or "").strip(),
        "example_pinyin": (payload.example_pinyin or "").strip(),
        "example_english": (payload.example_english or "").strip(),
        "created_by": user_id,
        "created_at": now,
    }
    await db.vocabulary.insert_one(doc)

    # Auto-add to user's deck
    await db.user_deck.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "vocabulary_id": vocab_id,
        "added_at": now,
    })

    doc.pop("_id", None)
    return doc


@api_router.delete("/vocabulary/custom/{vocab_id}")
async def delete_custom_vocab(vocab_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    vocab = await db.vocabulary.find_one({"id": vocab_id})
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")
    if vocab.get("created_by") != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own custom words")
    await db.vocabulary.delete_one({"id": vocab_id})
    await db.user_deck.delete_many({"vocabulary_id": vocab_id})
    await db.flashcards.delete_many({"vocabulary_id": vocab_id})
    return {"deleted": True}


# ---------- Vocabulary Library ----------
@api_router.get("/vocabulary/library")
async def vocabulary_library(
    q: Optional[str] = None,
    lesson_number: Optional[int] = None,
    source: Optional[str] = None,  # 'npcr' | 'custom'
    limit: int = 200,
    current_user: dict = Depends(get_current_user),
):
    """Browse the vocabulary library. Includes NPCR vocab + the user's custom vocab.
    Each item is annotated with `in_deck`."""
    user_id = current_user["id"]

    query: dict = {}
    if source == "npcr":
        query["lesson_number"] = {"$ne": None}
    elif source == "custom":
        query["created_by"] = user_id

    if lesson_number is not None:
        query["lesson_number"] = lesson_number

    if q:
        query["$or"] = [
            {"simplified": {"$regex": q, "$options": "i"}},
            {"pinyin": {"$regex": q, "$options": "i"}},
            {"english": {"$regex": q, "$options": "i"}},
        ]

    # NPCR vocab (lesson_id not null) + user's own custom vocab
    if source is None:
        query = {
            "$and": [
                query,
                {"$or": [{"lesson_id": {"$ne": None}}, {"created_by": user_id}]},
            ]
        }

    items = await db.vocabulary.find(query, {"_id": 0}).sort([("lesson_number", 1), ("created_at", -1)]).limit(limit).to_list(limit)

    deck_entries = await db.user_deck.find({"user_id": user_id}, {"vocabulary_id": 1, "_id": 0}).to_list(10000)
    deck_set = {e["vocabulary_id"] for e in deck_entries}

    for item in items:
        item["in_deck"] = item["id"] in deck_set
        item["is_custom"] = item.get("created_by") == user_id
    return items


# ---------- Writing / Handwriting Recognition ----------

def _ocr_score(target_norm: str, recognized_norm: str) -> tuple[int, bool]:
    """Score recognized text against target using bag-of-characters matching."""
    target_chars = list(target_norm)
    correct_chars = sum(1 for c in recognized_norm if c in target_chars)
    score = round((correct_chars / max(len(target_chars), 1)) * 100) if target_chars else 0
    exact_match = target_norm == recognized_norm and len(target_norm) > 0
    return score, exact_match


@api_router.post("/writing/recognize")
async def recognize_handwriting(payload: WritingRecognizeRequest, current_user: dict = Depends(get_current_user)):
    """Recognize handwritten Chinese characters using EasyOCR."""
    image_b64 = payload.image_base64
    if image_b64.startswith("data:"):
        _, _, image_b64 = image_b64.partition(",")
    if not image_b64 or len(image_b64) < 100:
        raise HTTPException(status_code=400, detail="Image is empty or invalid")

    target_norm = normalize_chinese(payload.target_chinese)

    try:
        image_bytes = b64lib.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(image)
        reader = _get_ocr_reader()
        loop = asyncio.get_event_loop()
        ocr_results = await loop.run_in_executor(
            None, lambda: reader.readtext(img_array, detail=0, paragraph=True)
        )
        recognized_raw = "".join(ocr_results)
        recognized_norm = normalize_chinese(recognized_raw)
    except Exception:
        logger.exception("OCR recognition failed")
        raise HTTPException(status_code=502, detail="OCR recognition failed")

    score, exact_match = _ocr_score(target_norm, recognized_norm)

    await db.writing_attempts.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": current_user["id"],
        "target_chinese": payload.target_chinese,
        "recognized_text": recognized_norm,
        "score": score,
        "identity_score": score,
        "quality_score": 0,
        "exact_match": exact_match,
        "vocabulary_id": payload.vocabulary_id,
        "timestamp": datetime.now(timezone.utc),
    })

    return {
        "correct": exact_match,
        "score": score,
        "identity_score": score,
        "quality_score": 0,
        "feedback": "",
        "characters": [],
        "recognized_text": recognized_norm,
        "target_text": payload.target_chinese,
    }


# ---------- Health ----------
@api_router.get("/")
async def root():
    return {"message": "Mandarin Learning API", "version": "1.0"}


app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
