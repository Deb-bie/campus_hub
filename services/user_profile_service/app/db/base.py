import os
from app.config import settings
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from pathlib import Path

DATABASE_URL = f"postgresql://{settings.DATABASE__USER}:{settings.DATABASE__PASSWORD}@{settings.DATABASE__HOST}:{settings.DATABASE__PORT}/{settings.DATABASE__NAME}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)