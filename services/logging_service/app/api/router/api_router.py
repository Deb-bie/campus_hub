from fastapi import APIRouter # type: ignore
from app.api.router import logs 

router = APIRouter()
router.include_router(logs.router, prefix="/api/logs", tags=["logs"])
