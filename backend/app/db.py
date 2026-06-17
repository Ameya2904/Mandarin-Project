"""MongoDB connection, index setup, and startup seeding/migration."""
import logging
import uuid
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient

from .config import DB_NAME, MONGO_URL
from .seed_data import NPCR_LESSONS, SENTENCE_DRILLS

logger = logging.getLogger(__name__)

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


async def deck_vocab_ids(user_id: str) -> set[str]:
    """The set of vocabulary ids currently in a user's deck."""
    rows = await db.user_deck.find(
        {"user_id": user_id}, {"vocabulary_id": 1, "_id": 0}
    ).to_list(10000)
    return {r["vocabulary_id"] for r in rows}


async def carded_vocab_ids(user_id: str) -> set[str]:
    """The set of vocabulary ids a user already has a flashcard for."""
    rows = await db.flashcards.find(
        {"user_id": user_id}, {"vocabulary_id": 1, "_id": 0}
    ).to_list(10000)
    return {r["vocabulary_id"] for r in rows}


async def create_indexes() -> None:
    """Create the indexes the app relies on (idempotent — safe every startup).

    The `unique=True` compound indexes are load-bearing: they enforce
    "one flashcard / one deck row per (user, word)" at the database level, which
    is what lets the add-to-deck and review code skip manual duplicate checks.
    The `next_review_at` index keeps the hot "cards due now" query fast.
    """
    await db.users.create_index("email", unique=True)
    await db.flashcards.create_index([("user_id", 1), ("vocabulary_id", 1)], unique=True)
    await db.flashcards.create_index([("user_id", 1), ("next_review_at", 1)])
    await db.user_deck.create_index([("user_id", 1), ("vocabulary_id", 1)], unique=True)
    await db.vocabulary.create_index("created_by")


async def seed_lessons_and_vocab() -> None:
    """Load the NPCR curriculum into the database (idempotent).

    Skips entirely when the lesson count already matches the seed file. When the
    count *differs* (e.g. you added lessons), it wipes and rebuilds only the
    content collections — user progress (decks, flashcards, accounts) is never
    touched, so re-seeding after a content edit is safe.
    """
    existing = await db.lessons.count_documents({})
    if existing == len(NPCR_LESSONS):
        logger.info(f"Lessons already seeded ({existing}). Skipping.")
        return

    if existing != len(NPCR_LESSONS) and existing > 0:
        logger.info(
            f"Lesson count changed ({existing} -> {len(NPCR_LESSONS)}). "
            "Reseeding lessons/vocab/drills (user data preserved)."
        )
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
                **vocab,
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


async def migrate_legacy_decks() -> None:
    """Back-fill user_deck for users who already have flashcards but no deck entries."""
    pipeline = [
        {"$group": {"_id": "$user_id", "vocab_ids": {"$addToSet": "$vocabulary_id"}}},
    ]
    cursor = db.flashcards.aggregate(pipeline)
    total = 0
    async for row in cursor:
        user_id = row["_id"]
        for vid in row["vocab_ids"]:
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
