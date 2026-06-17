"""Progress dashboard and stats endpoints."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from ..auth import get_current_user
from ..db import carded_vocab_ids, db, deck_vocab_ids

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/dashboard")
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    """Home-screen counts: due/new/mastered cards, today's reviews, and goal progress."""
    user_id = current_user["id"]
    now = datetime.now(timezone.utc)
    today_start = datetime.combine(now.date(), datetime.min.time()).replace(tzinfo=timezone.utc)

    due_count = await db.flashcards.count_documents({"user_id": user_id, "next_review_at": {"$lte": now}})
    total_cards = await db.flashcards.count_documents({"user_id": user_id})
    mastered = await db.flashcards.count_documents({"user_id": user_id, "current_stage": {"$gte": 4}})

    reviews_today = await db.review_history.count_documents(
        {"user_id": user_id, "timestamp": {"$gte": today_start}}
    )
    correct_today = await db.review_history.count_documents(
        {"user_id": user_id, "timestamp": {"$gte": today_start}, "was_correct": True}
    )

    # "New" = words the user has added to their deck but never reviewed yet
    # (no flashcard exists). Counting all vocabulary in the DB would include
    # words that aren't even in this user's deck.
    new_count = len(await deck_vocab_ids(user_id) - await carded_vocab_ids(user_id))
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


@router.get("/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    """Profile stats: retention rate, mastered/learning counts, and weak words."""
    user_id = current_user["id"]

    total_reviews = await db.review_history.count_documents({"user_id": user_id})
    correct_reviews = await db.review_history.count_documents({"user_id": user_id, "was_correct": True})
    retention = round((correct_reviews / total_reviews) * 100) if total_reviews > 0 else 0

    mastered = await db.flashcards.count_documents({"user_id": user_id, "current_stage": {"$gte": 4}})
    learning = await db.flashcards.count_documents({"user_id": user_id, "current_stage": {"$lt": 4}})

    # Weak words: cards missed more often than recalled. `$expr` lets us compare
    # two fields of the same document server-side.
    weak_cards = await db.flashcards.find(
        {"user_id": user_id, "$expr": {"$gt": ["$incorrect_count", "$correct_count"]}},
        {"_id": 0},
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
