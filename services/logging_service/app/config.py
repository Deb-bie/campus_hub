import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent

env = os.getenv("ENV", "development").lower()

env_file_map = {
    "development": BASE_DIR / ".env",
    "production": BASE_DIR / ".env.prod",
    "docker": BASE_DIR / ".env.docker"
}

selected_env_file = env_file_map.get(env, BASE_DIR / ".env")

class Settings(BaseSettings):
    PROJECT_NAME: str = "Campus Hub Logging Service"

    ENV: str
    DB_NAME: str
    DB_COLLECTION: str
    DB_USERNAME: str
    DB_PASSWORD: str
    KAFKA_BROKER: str
    KAFKA_TOPICS: list
    PORT: int


    model_config = SettingsConfigDict(
        env_file= ".env.dev",
        env_file_encoding="utf-8",
        extra="allow"
    )

settings = Settings(_env_file=selected_env_file)