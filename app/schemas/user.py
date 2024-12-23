from models.user import DigestFreq
from pydantic import BaseModel, Field, field_validator


class UserCreate(BaseModel):
    user_id: str
    username: str
    digest_freq: DigestFreq = DigestFreq.WEEKLY


class UserUpdateDigestParams(BaseModel):
    user_id: str
    digest_freq: DigestFreq
    digest_time: int = Field(..., ge=6, le=24)

    @field_validator("digest_time")
    def check_digest_time(cls, v):
        if not (6 <= v <= 24):
            raise ValueError("digest_time must be between 6 and 24")
        return v


class UserResponse(BaseModel):
    user_id: str
    username: str
    digest_freq: DigestFreq
    digest_time: int
    remaining_days: int | None
