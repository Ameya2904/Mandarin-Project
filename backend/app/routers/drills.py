"""Sentence-drill endpoints."""
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends

from ..auth import get_current_user
from ..db import db
from ..models import DrillAttemptRequest

router = APIRouter(prefix="/drills", tags=["drills"])

# Each drill is practised this many times in a row before moving on.
REPEAT_PER_DRILL = 3


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
    # Keep the seed's natural ordering so variants of the same pattern stay
    # grouped together (a guided "flow" rather than a random jumble), and
    # repeat each drill back-to-back so the learner drills it before moving on.
    drills = await db.drills.find(query, {"_id": 0}).to_list(2000)

    expanded = []
    for d in drills:
        for _ in range(REPEAT_PER_DRILL):
            expanded.append(d)
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
