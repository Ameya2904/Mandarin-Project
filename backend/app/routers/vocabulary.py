"""Custom vocabulary, library browsing, and semantic matching."""
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from ..auth import get_current_user
from ..db import db
from ..models import CustomVocabCreate, SemanticMatchRequest
from ..semantic import answer_matches_target

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"])


@router.post("/semantic-match")
async def check_semantic_match(
    payload: SemanticMatchRequest, current_user: dict = Depends(get_current_user)
):
    return {"match": answer_matches_target(payload.answer, payload.target)}


@router.post("/custom")
async def create_custom_vocab(
    payload: CustomVocabCreate, current_user: dict = Depends(get_current_user)
):
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


@router.delete("/custom/{vocab_id}")
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


@router.get("/library")
async def vocabulary_library(
    q: Optional[str] = None,
    lesson_number: Optional[int] = None,
    source: Optional[str] = None,  # 'npcr' | 'custom'
    limit: int = 200,
    current_user: dict = Depends(get_current_user),
):
    """Browse the vocabulary library: NPCR vocab + the user's custom vocab.
    Each item is annotated with `in_deck` and `is_custom`."""
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

    items = await db.vocabulary.find(query, {"_id": 0}).sort(
        [("lesson_number", 1), ("created_at", -1)]
    ).limit(limit).to_list(limit)

    deck_entries = await db.user_deck.find(
        {"user_id": user_id}, {"vocabulary_id": 1, "_id": 0}
    ).to_list(10000)
    deck_set = {e["vocabulary_id"] for e in deck_entries}

    for item in items:
        item["in_deck"] = item["id"] in deck_set
        item["is_custom"] = item.get("created_by") == user_id
    return items
