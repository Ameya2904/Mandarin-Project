"""Lesson endpoints."""
from fastapi import APIRouter, Depends, HTTPException

from ..auth import get_current_user
from ..db import db, deck_vocab_ids

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("")
async def list_lessons(current_user: dict = Depends(get_current_user)):
    """List every lesson, each annotated with this user's progress counts."""
    lessons = await db.lessons.find({}, {"_id": 0}).sort("lesson_number", 1).to_list(100)
    # Per lesson, count how many of its words this user has started/mastered.
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
    """Return one lesson with its full vocab, each word flagged `in_deck`."""
    lesson = await db.lessons.find_one({"id": lesson_id}, {"_id": 0})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    vocab = await db.vocabulary.find({"lesson_id": lesson_id}, {"_id": 0}).to_list(100)
    # Mark which vocab is in user's deck
    deck_set = await deck_vocab_ids(current_user["id"])
    for v in vocab:
        v["in_deck"] = v["id"] in deck_set
    lesson["vocabulary"] = vocab
    return lesson
