"""
Настройки базы данных.
"""

from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict

from app.infrastructure.settings.base import BaseAppSettings


class DatabaseSettings(BaseAppSettings):
    url: PostgresDsn

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
