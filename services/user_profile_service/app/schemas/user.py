from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr # type: ignore
from typing import Optional

class UserProfileBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserProfileCreate(UserProfileBase):
    user_id: UUID


class UserProfileUpdate(UserProfileBase):
    bio: str


class UserProfileResponse(UserProfileBase):
    user_id: UUID
    bio: str | None
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        from_attributes=True
