"""Authentication endpoints."""
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException

from ..auth import (
    create_access_token,
    get_current_user,
    hash_password,
    user_to_public,
    verify_password,
)
from ..db import db
from ..models import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserPublic,
    UserSettingsUpdate,
)

router = APIRouter(prefix="/auth", tags=["auth"])

RESET_TOKEN_TTL_MINUTES = 30


@router.post("/signup", response_model=TokenResponse)
async def signup(payload: UserCreate):
    """Create an account and return a JWT so the client is logged in immediately."""
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
    """Authenticate and return a JWT, updating the daily-login streak as a side effect."""
    email = payload.email.lower()
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(payload.password, user["hashed_password"]):
        # Same message whether the email or the password is wrong — don't reveal
        # which accounts exist.
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Streak rule: logging in on a consecutive day extends it, the same day
    # keeps it, and any gap resets it to 1.
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


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(payload: ForgotPasswordRequest):
    """Issue a short-lived reset token. Returned in the body (no mail service)."""
    email = payload.email.lower()
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="No account found with that email")

    token = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_TTL_MINUTES)
    await db.users.update_one(
        {"id": user["id"]},
        {"$set": {"reset_token": token, "reset_token_expires_at": expires_at}},
    )
    # NOTE: a production deployment would email this token instead of returning it.
    return ForgotPasswordResponse(
        reset_token=token, expires_in_minutes=RESET_TOKEN_TTL_MINUTES
    )


@router.post("/reset-password", response_model=TokenResponse)
async def reset_password(payload: ResetPasswordRequest):
    """Consume a valid reset token, set the new password, and log the user in."""
    user = await db.users.find_one({"reset_token": payload.token})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset code")

    expires_at = user.get("reset_token_expires_at")
    if not expires_at:
        raise HTTPException(status_code=400, detail="Invalid or expired reset code")
    if expires_at.tzinfo is None:
        # Mongo can hand back tz-naive datetimes; make it UTC-aware before comparing.
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired reset code")

    await db.users.update_one(
        {"id": user["id"]},
        {
            "$set": {"hashed_password": hash_password(payload.new_password)},
            "$unset": {"reset_token": "", "reset_token_expires_at": ""},
        },
    )

    token = create_access_token(user["id"])
    return TokenResponse(access_token=token, user=user_to_public(user))


@router.get("/me", response_model=UserPublic)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Return the current user's public profile."""
    return user_to_public(current_user)


@router.post("/change-password")
async def change_password(
    payload: ChangePasswordRequest, current_user: dict = Depends(get_current_user)
):
    """Change the password after verifying the current one."""
    # current_user is sanitized (no hashed_password), so re-fetch the full doc.
    user = await db.users.find_one({"id": current_user["id"]})
    if not user or not verify_password(payload.current_password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    await db.users.update_one(
        {"id": user["id"]},
        {"$set": {"hashed_password": hash_password(payload.new_password)}},
    )
    return {"success": True}


@router.put("/me", response_model=UserPublic)
async def update_me(payload: UserSettingsUpdate, current_user: dict = Depends(get_current_user)):
    """Patch settings (name / daily goal / level); only non-null fields are applied."""
    updates = {k: v for k, v in payload.dict().items() if v is not None}
    if updates:
        await db.users.update_one({"id": current_user["id"]}, {"$set": updates})
    refreshed = await db.users.find_one(
        {"id": current_user["id"]}, {"_id": 0, "hashed_password": 0}
    )
    return user_to_public(refreshed)
