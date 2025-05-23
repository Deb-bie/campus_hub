import os
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

class Settings(BaseSettings):
    API_V1: str = "/api/v1"
    PROJECT_NAME: str = "Campus Hub User Profile Service"

    DATABASE__USER: str
    DATABASE__PASSWORD: str
    DATABASE__HOST: str
    DATABASE__PORT: int
    DATABASE__NAME: str
    PORT: int
    ENV: str ="development"


    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        extra="allow"
    )

env = os.getenv("ENV", "development").lower()

env_file_map = {
    "development": ".env.dev",
    "production": ".env.prod",
    "docker": ".env.docker"
}

selected_env_file = env_file_map.get(env, ".env.dev")

settings = Settings(_env_file=selected_env_file)

