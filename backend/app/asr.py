"""Local speech-to-text via FunASR (Fun-ASR-Nano-2512).

The model is loaded lazily on first use and cached for the lifetime of the
process. Inference is CPU/GPU-bound and synchronous, so async callers MUST run
`transcribe()` inside a threadpool (see routers/speaking.py).
"""
import logging
import os
import subprocess
import tempfile
import threading

from .config import ASR_DEVICE, ASR_HUB, ASR_LANGUAGE, ASR_MODEL

logger = logging.getLogger(__name__)

_model = None
_model_lock = threading.Lock()   # guards one-time model load
_infer_lock = threading.Lock()   # serializes inference (model isn't thread-safe)


def _get_model():
    """Load the FunASR model once, then return the cached instance."""
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                from funasr import AutoModel

                logger.info("Loading FunASR model %s on %s ...", ASR_MODEL, ASR_DEVICE)
                # Fun-ASR-Nano ships custom code, so trust_remote_code is required.
                _model = AutoModel(
                    model=ASR_MODEL,
                    hub=ASR_HUB,
                    trust_remote_code=True,
                    device=ASR_DEVICE,
                    disable_update=True,
                )
                logger.info("FunASR model ready.")
    return _model


def warm_up() -> None:
    """Trigger model load eagerly (e.g. at server startup)."""
    _get_model()


def _to_wav_16k(src_path: str) -> str:
    """Convert any input audio to 16 kHz mono WAV via ffmpeg. Returns new path."""
    dst = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    dst.close()
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", src_path, "-ar", "16000", "-ac", "1", dst.name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        os.remove(dst.name)
        raise RuntimeError(f"ffmpeg conversion failed: {e.stderr.decode(errors='ignore')}") from e
    except FileNotFoundError as e:
        os.remove(dst.name)
        raise RuntimeError("ffmpeg not found on the server; install it with apt") from e
    return dst.name


def transcribe(audio_path: str, language: str = ASR_LANGUAGE) -> str:
    """Transcribe an audio file to text. Blocking — call via run_in_threadpool."""
    model = _get_model()
    wav_path = _to_wav_16k(audio_path)
    try:
        with _infer_lock:
            # itn=False: Inverse Text Normalization rewrites recognized sounds
            # into "written" forms (digits, Latin letters), which makes single
            # Mandarin syllables come back as homophonous English letters
            # (jī -> "G", bī -> "B"). We want raw Chinese characters here.
            res = model.generate(
                input=[wav_path],
                cache={},
                batch_size=1,
                language=language,
                itn=False,
            )
    finally:
        try:
            os.remove(wav_path)
        except OSError:
            pass

    if not res:
        return ""
    return (res[0].get("text") or "").strip()
