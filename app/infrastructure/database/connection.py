"""
Подготовка подключения к базе данных.
"""

from dataclasses import dataclass

from app.infrastructure.settings.database import DatabaseSettings


@dataclass(frozen=True)
class DatabaseConnectionInfo:
    url: str


def build_connection_info(settings: DatabaseSettings) -> DatabaseConnectionInfo:
    return DatabaseConnectionInfo(url=str(settings.url))
