from models.user import DigestFreq
from pydantic import BaseModel


class UserCreate(BaseModel):
    user_id: str
    username: str
    digest_freq: DigestFreq = DigestFreq.WEEKLY


class UserUpdateDigestFreq(BaseModel):
    user_id: str
    digest_freq: DigestFreq


class UserResponse(BaseModel):
    user_id: str
    username: str
    digest_freq: DigestFreq
    remaining_days: int | None
