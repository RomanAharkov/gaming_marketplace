from datetime import datetime, timezone
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        encoding="utf-8",
        extra="ignore"
    )

    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_NAME: str

    API_KEY: str

    APP_URL: str

    @staticmethod
    def get_current_time() -> datetime:
        return datetime.now(timezone.utc)


settings = Settings()

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@localhost:"
    f"{settings.DB_PORT}/{settings.DB_NAME}"
)