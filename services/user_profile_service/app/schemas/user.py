import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr # type: ignore
from typing import Optional

class UserProfileBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserProfileCreate(UserProfileBase):
    id: uuid
    

class UserProfileResponse(UserProfileBase):
    id: uuid
    bio: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode=True
