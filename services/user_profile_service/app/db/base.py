import os
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from dotenv import load_dotenv # type: ignore

dotenv_path = "../../.env"

load_dotenv(dotenv_path)

DATABASE__USER = os.getenv("DATABASE__USER")
DATABASE__PASSWORD = os.getenv("DATABASE__PASSWORD")
DATABASE__HOST = os.getenv("DATABASE__HOST")
DATABASE__PORT = os.getenv("DATABASE__PORT")
DATABASE__NAME = os.getenv("DATABASE__NAME")

DATABASE_URL = f"postgresql://{DATABASE__USER}:{DATABASE__PASSWORD}@{DATABASE__HOST}:{DATABASE__PORT}/{DATABASE__NAME}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


