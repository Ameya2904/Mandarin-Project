"""User deck management endpoints."""
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from ..auth import get_current_user
from ..db import db
from ..models import DeckAddRequest

router = APIRouter(prefix="/deck", tags=["deck"])


@router.get("")
async def list_deck(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    deck = await db.user_deck.find({"user_id": user_id}, {"_id": 0}).sort("added_at", -1).to_list(10000)
    result = []
    for entry in deck:
        vocab = await db.vocabulary.find_one({"id": entry["vocabulary_id"]}, {"_id": 0})
        if vocab:
            card = await db.flashcards.find_one(
                {"user_id": user_id, "vocabulary_id": entry["vocabulary_id"]}, {"_id": 0}
            )
            result.append({
                **entry,
                "vocabulary": vocab,
                "current_stage": card.get("current_stage") if card else None,
                "next_review_at": card.get("next_review_at").isoformat()
                if card and card.get("next_review_at") else None,
            })
    return result


@router.post("/add")
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


@router.delete("/{vocabulary_id}")
async def remove_from_deck(vocabulary_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    deck_res = await db.user_deck.delete_one({"user_id": user_id, "vocabulary_id": vocabulary_id})
    # Also remove their flashcard for this word
    await db.flashcards.delete_one({"user_id": user_id, "vocabulary_id": vocabulary_id})
    return {"removed": deck_res.deleted_count > 0}
