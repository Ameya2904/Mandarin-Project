"""Pydantic request/response models.

These classes are the typed contract between the API and its clients. FastAPI
uses them to validate incoming JSON (rejecting bad requests with a 422 before
any handler runs) and to serialize responses. Keep them in sync with the
TypeScript types in `frontend/src/api/client.ts`.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Signup payload. `Field` constraints reject weak input before hashing."""

    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=1)


class UserLogin(BaseModel):
    """Login payload."""

    email: EmailStr
    password: str


class UserPublic(BaseModel):
    """The safe, client-facing shape of a user — never includes the password.

    Defaults let a partial/legacy user document still serialize cleanly.
    """

    id: str
    email: str
    name: str
    daily_goal: int = 20
    streak_count: int = 0
    created_at: datetime


class TokenResponse(BaseModel):
    """Returned by signup/login/reset — a JWT plus the public user."""

    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class CustomVocabCreate(BaseModel):
    """Payload for a user-authored vocabulary word."""

    simplified: str = Field(min_length=1)
    pinyin: str = Field(min_length=1)
    english: str = Field(min_length=1)
    example_chinese: Optional[str] = ""
    example_pinyin: Optional[str] = ""
    example_english: Optional[str] = ""
    part_of_speech: Optional[str] = "custom"


class DeckAddRequest(BaseModel):
    """Bulk-add request — a list of vocabulary ids to put in the user's deck."""

    vocabulary_ids: List[str]


class WritingRecognizeRequest(BaseModel):
    """A handwriting submission: the drawn image plus what it should spell."""

    image_base64: str
    target_chinese: str
    vocabulary_id: Optional[str] = None


class FlashcardReviewRequest(BaseModel):
    """A single review result.

    `mode` records which modality was tested. `skip_srs` lets a caller log the
    attempt to history *without* advancing the spaced-repetition stage — used so
    that only the final mode of a multi-mode review reschedules the card.
    """

    vocabulary_id: str
    was_correct: bool
    response_time_ms: Optional[int] = None
    mode: Optional[str] = "reading"  # reading | writing | speaking
    skip_srs: bool = False  # log history only, don't advance SRS stage


class DrillAttemptRequest(BaseModel):
    """A logged attempt at a sentence drill (scored client-side via speaking)."""

    drill_id: str
    user_answer: str
    was_correct: bool
    response_time_ms: Optional[int] = None


class SemanticMatchRequest(BaseModel):
    """Ask whether a free-text English `answer` is a synonym of `target`."""

    answer: str
    target: str


class UserSettingsUpdate(BaseModel):
    """Partial settings update — only non-null fields are applied."""

    name: Optional[str] = None
    daily_goal: Optional[int] = None
    learner_level: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    """Step 1 of password reset: the account email."""

    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    """The reset token, returned directly because this app has no mail service.

    In production the token would be emailed, not put in the response body; it
    is surfaced here only so the reset flow is usable without email.
    """

    reset_token: str
    expires_in_minutes: int


class ResetPasswordRequest(BaseModel):
    """Step 2 of password reset: the token plus the new password."""

    token: str
    new_password: str = Field(min_length=6)


class ChangePasswordRequest(BaseModel):
    """In-app password change for a logged-in user."""

    current_password: str
    new_password: str = Field(min_length=6)
