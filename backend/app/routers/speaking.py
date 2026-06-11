"""Speaking practice: FunASR transcription + pronunciation scoring."""
import logging
import os
import tempfile
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from .. import asr
from ..auth import get_current_user
from ..db import db
from ..scoring import (
    normalize_chinese,
    pinyin_display,
    pronunciation_feedback,
    score_pronunciation,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/speaking", tags=["speaking"])

_ALLOWED_AUDIO_SUFFIXES = {"mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"}


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    target_chinese: str = "",
    vocabulary_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
):
    """Accept an audio file (m4a/wav/webm), transcribe it with FunASR, then
    compare to target_chinese (if provided) for pronunciation feedback."""
    filename = file.filename or "audio.m4a"
    suffix = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ".m4a"
    if suffix.lstrip(".") not in _ALLOWED_AUDIO_SUFFIXES:
        suffix = ".m4a"

    contents = await file.read()
    if len(contents) > 25 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Audio file too large (max 25MB)")
    if len(contents) < 100:
        raise HTTPException(status_code=400, detail="Audio file too small / empty")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(contents)
    tmp.close()

    try:
        transcribed = await run_in_threadpool(asr.transcribe, tmp.name)
    except Exception as e:
        logger.exception("Transcription failed")
        raise HTTPException(status_code=502, detail=f"Transcription failed: {str(e)}")
    finally:
        try:
            os.remove(tmp.name)
        except OSError:
            pass

    transcribed = (transcribed or "").strip()

    result = {"transcribed_text": transcribed}
    if target_chinese:
        target_norm = normalize_chinese(target_chinese)
        spoken_norm = normalize_chinese(transcribed)

        # Syllable-level pinyin scoring: full credit when sound + tone match,
        # half credit when the syllable is right but the tone is wrong. This
        # also handles homophones (same pinyin, different characters).
        p = score_pronunciation(target_norm, spoken_norm)

        await db.speaking_attempts.insert_one({
            "id": str(uuid.uuid4()),
            "user_id": current_user["id"],
            "target_chinese": target_chinese,
            "spoken_text": transcribed,
            "score": p["score"],
            "exact_match": p["correct"],
            "vocabulary_id": vocabulary_id,
            "source": "funasr",
            "timestamp": datetime.now(timezone.utc),
        })

        result.update({
            "correct": p["correct"],
            "score": p["score"],
            "feedback": pronunciation_feedback(p),
            "target_text": target_chinese,
            "target_pinyin": pinyin_display(target_norm),
            "spoken_pinyin": pinyin_display(spoken_norm) if spoken_norm else "",
            "tones_wrong": p["tones_wrong"],
            "syllables_right": p["syllables_right"],
            "syllable_count": p["total"],
        })

    return result
