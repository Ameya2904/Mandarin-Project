"""Flashcard / spaced-repetition endpoints."""
import uuid
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from ..auth import get_current_user
from ..config import SRS_INTERVALS
from ..db import carded_vocab_ids, db, deck_vocab_ids
from ..models import FlashcardReviewRequest

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.get("/due")
async def get_due_flashcards(limit: int = 20, current_user: dict = Depends(get_current_user)):
    """Get cards due for review today (or earlier)."""
    now = datetime.now(timezone.utc)
    cards = await db.flashcards.find(
        {"user_id": current_user["id"], "next_review_at": {"$lte": now}},
        {"_id": 0},
    ).sort("next_review_at", 1).limit(limit).to_list(limit)

    result = []
    for card in cards:
        vocab = await db.vocabulary.find_one({"id": card["vocabulary_id"]}, {"_id": 0})
        if vocab:
            result.append({**card, "vocabulary": vocab})
    return result


@router.get("/new")
async def get_new_flashcards(
    lesson_id: Optional[str] = None, limit: int = 10, current_user: dict = Depends(get_current_user)
):
    """Get vocabulary words the user has added to deck but never reviewed yet."""
    user_id = current_user["id"]

    deck_ids = await deck_vocab_ids(user_id)
    if not deck_ids:
        return []

    existing_ids = await carded_vocab_ids(user_id)
    new_ids = list(deck_ids - existing_ids)
    if not new_ids:
        return []

    query: dict = {"id": {"$in": new_ids}}
    if lesson_id:
        query["lesson_id"] = lesson_id

    return await db.vocabulary.find(query, {"_id": 0}).sort("lesson_number", 1).limit(limit).to_list(limit)


@router.get("/schedule")
async def get_review_schedule(days: int = 14, current_user: dict = Depends(get_current_user)):
    """Return how many cards are due on each upcoming day (next `days` days)."""
    user_id = current_user["id"]
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)

    cards = await db.flashcards.find(
        {"user_id": user_id, "next_review_at": {"$gte": now, "$lte": end}},
        {"_id": 0, "next_review_at": 1},
    ).to_list(5000)

    counts: dict = defaultdict(int)
    for card in cards:
        counts[card["next_review_at"].strftime("%Y-%m-%d")] += 1

    schedule = []
    for i in range(days):
        # i + 1: the schedule starts tomorrow — today's due cards are "due now",
        # not "upcoming".
        date_key = (now + timedelta(days=i + 1)).date().strftime("%Y-%m-%d")
        if date_key in counts:
            schedule.append({"date": date_key, "count": counts[date_key]})
    return schedule


@router.post("/review")
async def submit_review(
    payload: FlashcardReviewRequest, current_user: dict = Depends(get_current_user)
):
    """Record one review and move the card through the spaced-repetition ladder.

    The stage rules:
      - Correct: advance one stage (capped at 6, the longest interval).
      - Incorrect: reset to stage 1 — a missed word is treated as new again.
      - A word's very first review starts at stage 2 (correct) or 1 (incorrect).
    `next_review_at` is then `now + SRS_INTERVALS[stage]` days.

    If `payload.skip_srs` is set, the attempt is only logged to history and the
    stage is left untouched — this is how the non-final modes of a multi-mode
    review avoid advancing the card three times for one word.
    """
    user_id = current_user["id"]
    now = datetime.now(timezone.utc)

    vocab = await db.vocabulary.find_one({"id": payload.vocabulary_id})
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")

    existing = await db.flashcards.find_one(
        {"user_id": user_id, "vocabulary_id": payload.vocabulary_id}
    )

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
            }},
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
