"""Sentence-drill endpoints."""
import random
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends

from ..auth import get_current_user
from ..db import db
from ..models import DrillAttemptRequest

router = APIRouter(prefix="/drills", tags=["drills"])


@router.get("")
async def list_drills(
    lesson_number: Optional[int] = None,
    part: Optional[int] = None,
    limit: int = 500,
    current_user: dict = Depends(get_current_user),
):
    query: dict = {}
    if lesson_number is not None:
        query["lesson_number"] = lesson_number
    if part is not None:
        query["part"] = part
    drills = await db.drills.find(query, {"_id": 0}).to_list(2000)

    expanded = []
    for d in drills:
        n = max(1, int(d.get("repeat_count", 1)))
        for _ in range(n):
            expanded.append(d)
    random.shuffle(expanded)
    return expanded[:limit]


@router.post("/attempt")
async def submit_drill_attempt(
    payload: DrillAttemptRequest, current_user: dict = Depends(get_current_user)
):
    await db.drill_attempts.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": current_user["id"],
        "drill_id": payload.drill_id,
        "user_answer": payload.user_answer,
        "was_correct": payload.was_correct,
        "response_time_ms": payload.response_time_ms,
        "timestamp": datetime.now(timezone.utc),
    })
    return {"success": True}
