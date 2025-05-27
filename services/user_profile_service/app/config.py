import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent

env = os.getenv("ENV", "development").lower()

env_file_map = {
    "development": BASE_DIR / ".env.dev",
    "production": BASE_DIR / ".env.prod",
    "docker": BASE_DIR / ".env.docker"
}

selected_env_file = env_file_map.get(env, BASE_DIR / ".env.dev")

class Settings(BaseSettings):
    API_V1: str = "/api/v1"
    PROJECT_NAME: str = "Campus Hub User Profile Service"

    DATABASE__USER: str
    DATABASE__PASSWORD: str
    DATABASE__HOST: str
    DATABASE__PORT: int
    DATABASE__NAME: str
    JWT__SECRET__KEY: str
    ALGORITHM: str
    PORT: int
    ENV: str ="development"


    model_config = SettingsConfigDict(
        env_file= ".env.dev",
        env_file_encoding="utf-8",
        extra="allow"
    )


settings = Settings(_env_file=selected_env_file)

