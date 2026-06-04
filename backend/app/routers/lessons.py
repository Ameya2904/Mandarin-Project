"""Lesson endpoints."""
from fastapi import APIRouter, Depends, HTTPException

from ..auth import get_current_user
from ..db import db

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("")
async def list_lessons(current_user: dict = Depends(get_current_user)):
    lessons = await db.lessons.find({}, {"_id": 0}).sort("lesson_number", 1).to_list(100)
    # Add progress info per lesson
    for lesson in lessons:
        vocab_ids = lesson.get("vocabulary_ids", [])
        if vocab_ids:
            mastered = await db.flashcards.count_documents({
                "user_id": current_user["id"],
                "vocabulary_id": {"$in": vocab_ids},
                "current_stage": {"$gte": 4},
            })
            started = await db.flashcards.count_documents({
                "user_id": current_user["id"],
                "vocabulary_id": {"$in": vocab_ids},
            })
            lesson["progress"] = {"mastered": mastered, "started": started, "total": len(vocab_ids)}
        else:
            lesson["progress"] = {"mastered": 0, "started": 0, "total": 0}
    return lessons


@router.get("/{lesson_id}")
async def get_lesson(lesson_id: str, current_user: dict = Depends(get_current_user)):
    lesson = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    vocab = await db.vocabulary.find({"lesson_id": lesson_id}, {"_id": 0}).to_list(100)
    # Mark which vocab is in user's deck
    deck_entries = await db.user_deck.find(
        {"user_id": current_user["id"]}, {"vocabulary_id": 1, "_id": 0}
    ).to_list(10000)
    deck_set = {e["vocabulary_id"] for e in deck_entries}
    for v in vocab:
        v["in_deck"] = v["id"] in deck_set
    lesson["vocabulary"] = vocab
    return lesson
