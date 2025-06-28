from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from contextlib import asynccontextmanager
from typing import Optional
from app.config import settings
from app.db.db import collection
from app.services.consumer import start_consumer_thread
from app.api.router.api_router import router as api_router
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=== ENVIRONMENT VARIABLES ===")
    print(f"ENV: {os.getenv('ENV')}")
    print(f"KAFKA_BROKER: {os.getenv('KAFKA_BROKER')}")
    print(f"KAFKA_TOPICS: {os.getenv('KAFKA_TOPICS')}")
    print(f"PORT: {os.getenv('PORT')}")
    print("=============================")

    # Startup logic
    start_consumer_thread()
    yield
    # Shutdown logic (optional cleanup)
    print("Shutting down Logging Service...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router)

@app.get("/")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn # type: ignore
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.PORT
    )


