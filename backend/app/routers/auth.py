"""Authentication endpoints."""
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from ..auth import (
    create_access_token,
    get_current_user,
    hash_password,
    user_to_public,
    verify_password,
)
from ..db import db
from ..models import TokenResponse, UserCreate, UserLogin, UserPublic, UserSettingsUpdate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
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


@router.post("/login", response_model=TokenResponse)
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
        {"$set": {"last_active_date": today.isoformat(), "streak_count": new_streak}},
    )
    user["streak_count"] = new_streak

    token = create_access_token(user["id"])
    return TokenResponse(access_token=token, user=user_to_public(user))


@router.get("/me", response_model=UserPublic)
async def get_me(current_user: dict = Depends(get_current_user)):
    return user_to_public(current_user)


@router.put("/me", response_model=UserPublic)
async def update_me(payload: UserSettingsUpdate, current_user: dict = Depends(get_current_user)):
    updates = {k: v for k, v in payload.dict().items() if v is not None}
    if updates:
        await db.users.update_one({"id": current_user["id"]}, {"$set": updates})
    refreshed = await db.users.find_one(
        {"id": current_user["id"]}, {"_id": 0, "hashed_password": 0}
    )
    return user_to_public(refreshed)
