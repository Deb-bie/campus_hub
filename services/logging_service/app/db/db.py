import os
from motor.motor_asyncio import AsyncIOMotorClient # type: ignore
from app.config import settings


DB_URL = f"mongodb+srv://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@cluster0.wgt5ozf.mongodb.net/{settings.DB_NAME}?retryWrites=true&w=majority&appName=Cluster0"

client = AsyncIOMotorClient(DB_URL)
db = client[settings.DB_NAME]
collection = db[settings.DB_COLLECTION]