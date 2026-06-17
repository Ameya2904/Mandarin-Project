"""Mandarin Learning App — FastAPI application entry point.

Run with:  uvicorn app.main:app --reload   (from the backend/ directory)
"""
import logging

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from . import asr
from .db import client, create_indexes, migrate_legacy_decks, seed_lessons_and_vocab
from .routers import (
    auth,
    deck,
    drills,
    flashcards,
    lessons,
    progress,
    speaking,
    vocabulary,
    writing,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mandarin Learning API")

api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    """Unauthenticated liveness check at GET /api/."""
    return {"message": "Mandarin Learning API", "version": "1.0"}


for module in (auth, lessons, flashcards, drills, deck, vocabulary, speaking, writing, progress):
    api_router.include_router(module.router)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """Prepare the database and AI models before serving traffic.

    Order matters: indexes (and their unique constraints) must exist before we
    seed content, and seeding must finish before the legacy-deck migration reads
    it. The ASR warm-up is last so a cold model load doesn't delay startup-time
    DB work — it just front-loads the cost off the first user request.
    """
    await create_indexes()
    await seed_lessons_and_vocab()
    await migrate_legacy_decks()
    asr.warm_up()  # load the ASR model now so the first request isn't slow


@app.on_event("shutdown")
async def on_shutdown():
    """Close the MongoDB client cleanly on shutdown."""
    client.close()
