"""Pydantic request/response models."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=1)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: str
    email: str
    name: str
    daily_goal: int = 20
    streak_count: int = 0
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class CustomVocabCreate(BaseModel):
    simplified: str = Field(min_length=1)
    pinyin: str = Field(min_length=1)
    english: str = Field(min_length=1)
    example_chinese: Optional[str] = ""
    example_pinyin: Optional[str] = ""
    example_english: Optional[str] = ""
    part_of_speech: Optional[str] = "custom"


class DeckAddRequest(BaseModel):
    vocabulary_ids: List[str]


class WritingRecognizeRequest(BaseModel):
    image_base64: str
    target_chinese: str
    vocabulary_id: Optional[str] = None


class FlashcardReviewRequest(BaseModel):
    vocabulary_id: str
    was_correct: bool
    response_time_ms: Optional[int] = None
    mode: Optional[str] = "reading"  # reading | writing | speaking
    skip_srs: bool = False  # log history only, don't advance SRS stage


class DrillAttemptRequest(BaseModel):
    drill_id: str
    user_answer: str
    was_correct: bool
    response_time_ms: Optional[int] = None


class SemanticMatchRequest(BaseModel):
    answer: str
    target: str


class UserSettingsUpdate(BaseModel):
    name: Optional[str] = None
    daily_goal: Optional[int] = None
    learner_level: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    # In production the reset token would be emailed, not returned in the body.
    # This app has no mail service, so we surface it so the flow is usable.
    reset_token: str
    expires_in_minutes: int


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=6)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)
