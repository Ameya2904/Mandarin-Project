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

# ---------- Setup ----------
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

JWT_SECRET = os.environ['JWT_SECRET_KEY']
JWT_ALGO = os.environ.get('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 43200))
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

app = FastAPI(title="Mandarin Learning API")
api_router = APIRouter(prefix="/api")
security = HTTPBearer(auto_error=False)

# Stage intervals in days for spaced repetition
SRS_INTERVALS = {1: 1, 2: 2, 3: 7, 4: 30, 5: 90, 6: 365}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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


class FlashcardReviewRequest(BaseModel):
    vocabulary_id: str
    was_correct: bool
    response_time_ms: Optional[int] = None


class DrillAttemptRequest(BaseModel):
    drill_id: str
    user_answer: str
    was_correct: bool
    response_time_ms: Optional[int] = None


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
    if existing > 0:
        logger.info(f"Lessons already seeded ({existing}). Skipping.")
        return

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
    await seed_lessons_and_vocab()


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
    """Get vocabulary words the user has never reviewed yet."""
    user_id = current_user["id"]
    existing = await db.flashcards.find({"user_id": user_id}, {"vocabulary_id": 1, "_id": 0}).to_list(10000)
    existing_ids = {e["vocabulary_id"] for e in existing}

    query = {"id": {"$nin": list(existing_ids)}}
    if lesson_id:
        query["lesson_id"] = lesson_id

    vocab_list = await db.vocabulary.find(query, {"_id": 0}).sort("lesson_number", 1).limit(limit).to_list(limit)
    return vocab_list


@api_router.post("/flashcards/review")
async def submit_review(payload: FlashcardReviewRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    now = datetime.now(timezone.utc)

    vocab = await db.vocabulary.find_one({"id": payload.vocabulary_id})
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")

    existing = await db.flashcards.find_one({"user_id": user_id, "vocabulary_id": payload.vocabulary_id})

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
        "timestamp": now,
    })

    return {"success": True, "new_stage": new_stage, "next_review_at": next_review.isoformat()}


# ---------- Drill Endpoints ----------
@api_router.get("/drills")
async def list_drills(lesson_number: Optional[int] = None, limit: int = 20, current_user: dict = Depends(get_current_user)):
    query = {}
    if lesson_number is not None:
        query["lesson_number"] = lesson_number
    drills = await db.drills.find(query, {"_id": 0}).limit(limit).to_list(limit)
    return drills


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


@api_router.post("/speaking/evaluate")
async def evaluate_speaking(payload: SpeakingAttemptRequest, current_user: dict = Depends(get_current_user)):
    """Compare spoken text against target sentence."""
    target_normalized = normalize_chinese(payload.target_chinese)
    spoken_normalized = normalize_chinese(payload.spoken_text)

    if not spoken_normalized:
        return {"correct": False, "score": 0, "feedback": "No speech detected. Try again.", "spoken_text": payload.spoken_text}

    # Character-level overlap
    target_chars = list(target_normalized)
    spoken_chars = list(spoken_normalized)

    correct_chars = sum(1 for c in spoken_chars if c in target_chars)
    score = round((correct_chars / max(len(target_chars), 1)) * 100)
    exact_match = target_normalized == spoken_normalized

    if exact_match:
        feedback = "Perfect! 完美!"
    elif score >= 80:
        feedback = "Great pronunciation! Almost there."
    elif score >= 50:
        feedback = "Good attempt. Some characters were off."
    else:
        feedback = "Try again. Listen carefully to the target."

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
