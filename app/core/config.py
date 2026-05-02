from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Core application settings.
    """

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    NAME: str = "Data Ingestion Service"
    ENV: Literal["development", "production"] = "development"
    API_VERSION_PREFIX: str = "/api/v1"
    DEBUG: bool = True


class CORSSettings(BaseSettings):
    """
    CORS configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="CORS_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ALLOW_ORIGINS: list[str] = ["127.0.0.1", "localhost"]
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True


class DatabaseSettings(BaseSettings):
    """
    Database configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    NAME: str = "app"

    @property
    def async_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )

    @property
    def sync_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )


class Settings:
    """
    Central configuration container.
    """

    def __init__(self) -> None:
        self.app = AppSettings()
        self.cors = CORSSettings()
        self.db = DatabaseSettings()


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    """
    return Settings()
