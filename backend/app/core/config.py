from datetime import datetime, timedelta, timezone
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
    DB_HOST: str
    DB_NAME: str

    API_KEY: str

    APP_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    @staticmethod
    def get_current_time() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def get_access_token_expire_minutes() -> timedelta:
        return timedelta(minutes=1)


settings = Settings()

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_NAME}"
)