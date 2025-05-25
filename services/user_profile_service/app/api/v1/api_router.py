from fastapi import APIRouter # type: ignore
from app.api.v1.endpoints import users

router = APIRouter()

router.include_router(users.router, prefix="/users/profile", tags=["users"])
