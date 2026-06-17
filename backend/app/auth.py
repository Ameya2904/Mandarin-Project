"""Authentication helpers and the current-user dependency."""
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGO, JWT_SECRET
from .db import db
from .models import UserPublic

security = HTTPBearer(auto_error=False)


def hash_password(plain: str) -> str:
    """Hash a plaintext password with bcrypt (a fresh random salt per call)."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Check a password against its bcrypt hash.

    Returns False on any error (e.g. a malformed stored hash) so a corrupt
    record can never crash login — it just fails authentication.
    """
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_access_token(user_id: str) -> str:
    """Sign a JWT carrying the user id (`sub`) and an expiry (`exp`)."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


async def get_current_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """FastAPI dependency that resolves the bearer token to a user document.

    Injected into every protected route via `Depends(get_current_user)`; that
    single dependency is what gates the whole API. Raises 401 if the token is
    missing, invalid, expired, or points at a deleted user. The returned
    document is sanitized (no `_id`, no `hashed_password`) — which is why
    routes needing the hash (e.g. change-password) must re-fetch it.
    """
    if creds is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALGO])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        # Covers bad signature, malformed token, and expiry in one place.
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await db.users.find_one({"id": user_id}, {"_id": 0, "hashed_password": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def user_to_public(doc: dict) -> UserPublic:
    """Map a raw user document to the safe, client-facing `UserPublic` shape."""
    return UserPublic(
        id=doc["id"],
        email=doc["email"],
        name=doc["name"],
        daily_goal=doc.get("daily_goal", 20),
        streak_count=doc.get("streak_count", 0),
        created_at=doc["created_at"],
    )
