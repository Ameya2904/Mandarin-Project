"""Handwriting recognition via EasyOCR."""
import asyncio
import base64 as b64lib
import io
import logging
import uuid
from datetime import datetime, timezone

import easyocr
import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from PIL import Image

from ..auth import get_current_user
from ..db import db
from ..models import WritingRecognizeRequest
from ..scoring import normalize_chinese

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/writing", tags=["writing"])

# Lazy-initialized EasyOCR reader (loads ~100MB models on first use).
_ocr_reader: easyocr.Reader | None = None


def _get_ocr_reader() -> easyocr.Reader:
    global _ocr_reader
    if _ocr_reader is None:
        logger.info("Initializing EasyOCR reader (first use)...")
        _ocr_reader = easyocr.Reader(["ch_sim"], gpu=False)
    return _ocr_reader


def _ocr_score(target_norm: str, recognized_norm: str) -> tuple[int, bool]:
    """Score recognized text against target using bag-of-characters matching."""
    target_chars = list(target_norm)
    correct_chars = sum(1 for c in recognized_norm if c in target_chars)
    score = round((correct_chars / max(len(target_chars), 1)) * 100) if target_chars else 0
    exact_match = target_norm == recognized_norm and len(target_norm) > 0
    return score, exact_match


@router.post("/recognize")
async def recognize_handwriting(
    payload: WritingRecognizeRequest, current_user: dict = Depends(get_current_user)
):
    """Recognize handwritten Chinese characters using EasyOCR."""
    image_b64 = payload.image_base64
    if image_b64.startswith("data:"):
        _, _, image_b64 = image_b64.partition(",")
    if not image_b64 or len(image_b64) < 100:
        raise HTTPException(status_code=400, detail="Image is empty or invalid")

    target_norm = normalize_chinese(payload.target_chinese)

    try:
        image_bytes = b64lib.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(image)
        reader = _get_ocr_reader()
        loop = asyncio.get_event_loop()
        ocr_results = await loop.run_in_executor(
            None, lambda: reader.readtext(img_array, detail=0, paragraph=True)
        )
        recognized_norm = normalize_chinese("".join(ocr_results))
    except Exception:
        logger.exception("OCR recognition failed")
        raise HTTPException(status_code=502, detail="OCR recognition failed")

    score, exact_match = _ocr_score(target_norm, recognized_norm)

    await db.writing_attempts.insert_one({
        "id": str(uuid.uuid4()),
        "user_id": current_user["id"],
        "target_chinese": payload.target_chinese,
        "recognized_text": recognized_norm,
        "score": score,
        "identity_score": score,
        "quality_score": 0,
        "exact_match": exact_match,
        "vocabulary_id": payload.vocabulary_id,
        "timestamp": datetime.now(timezone.utc),
    })

    return {
        "correct": exact_match,
        "score": score,
        "identity_score": score,
        "quality_score": 0,
        "feedback": "",
        "characters": [],
        "recognized_text": recognized_norm,
        "target_text": payload.target_chinese,
    }
