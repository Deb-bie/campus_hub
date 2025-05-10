import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr # type: ignore
from typing import Optional

class UserProfileBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserProfileResponse(UserProfileBase):
    id: uuid
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_loggedIn: Optional[datetime]

    class Config:
        orm_mode=True
