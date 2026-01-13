# FastAPI Clean Architecture Template

## Структура репозитория

```
.
├── Dockerfile
├── README.md
├── app
│   ├── __init__.py
│   ├── application
│   │   ├── __init__.py
│   │   ├── dto
│   │   │   ├── __init__.py
│   │   │   └── message_dto.py
│   │   ├── interfaces
│   │   │   └── __init__.py
│   │   └── use_cases
│   │       ├── __init__.py
│   │       └── get_message.py
│   ├── container.py
│   ├── domain
│   │   ├── __init__.py
│   │   ├── entities
│   │   │   ├── __init__.py
│   │   │   └── message.py
│   │   ├── repositories
│   │   │   ├── __init__.py
│   │   │   └── message_repository.py
│   │   ├── services
│   │   │   └── __init__.py
│   │   └── value_objects
│   │       └── __init__.py
│   ├── infrastructure
│   │   ├── __init__.py
│   │   ├── database
│   │   │   ├── __init__.py
│   │   │   └── connection.py
│   │   ├── redis
│   │   │   ├── __init__.py
│   │   │   └── client.py
│   │   ├── repositories
│   │   │   ├── __init__.py
│   │   │   └── static_message_repository.py
│   │   └── settings
│   │       ├── __init__.py
│   │       ├── app.py
│   │       ├── base.py
│   │       ├── database.py
│   │       └── redis.py
│   ├── main.py
│   └── presentation
│       ├── __init__.py
│       ├── api
│       │   ├── __init__.py
│       │   ├── dependencies
│       │   │   ├── __init__.py
│       │   │   └── container.py
│       │   └── v1
│       │       ├── __init__.py
│       │       ├── health.py
│       │       ├── messages.py
│       │       └── router.py
│       └── schemas
│           ├── __init__.py
│           ├── health.py
│           └── message.py
├── docker
│   └── entrypoint.sh
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
├── tests
│   ├── application
│   │   └── .gitkeep
│   ├── domain
│   │   └── .gitkeep
│   └── presentation
│       ├── test_health.py
│       └── test_message.py
└── .env.example
```

## Ключевые файлы

### Dockerfile

```
FROM python:3.12-slim

ENV POETRY_VERSION=2.1.4 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential postgresql-client \
    && pip install "poetry==${POETRY_VERSION}" \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

COPY app ./app
COPY docker/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```
services:
  backend:
    build: .
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: app_password
      POSTGRES_DB: app_db
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app_user -d app_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### app/main.py

```
"""
Точка входа FastAPI приложения.
"""

from fastapi import FastAPI

from app.container import Container
from app.presentation.api.v1.router import router as v1_router


def create_app() -> FastAPI:
    container = Container()
    app = FastAPI(title=container.settings.name, debug=container.settings.debug)
    app.include_router(v1_router, prefix="/api/v1")
    return app


app = create_app()
```

### app/container.py

```
"""
Контейнер зависимостей приложения.
"""

from app.application.use_cases.get_message import GetMessageUseCase
from app.infrastructure.repositories.static_message_repository import StaticMessageRepository
from app.infrastructure.settings.app import AppSettings, load_settings


class Container:
    def __init__(self) -> None:
        self._settings = load_settings()
        self._message_repository = StaticMessageRepository(
            message_text="FastAPI clean architecture template",
            message_source=self._settings.name,
        )
        self._get_message_use_case = GetMessageUseCase(self._message_repository)

    @property
    def settings(self) -> AppSettings:
        return self._settings

    @property
    def get_message_use_case(self) -> GetMessageUseCase:
        return self._get_message_use_case
```

### app/infrastructure/settings/app.py

```
"""
Настройки приложения.
"""

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from app.infrastructure.settings.base import BaseAppSettings
from app.infrastructure.settings.database import DatabaseSettings
from app.infrastructure.settings.redis import RedisSettings


class AppSettings(BaseAppSettings):
    name: str = Field(default="FastAPI Clean Template", validation_alias="APP_NAME")
    environment: str = Field(default="local", validation_alias="APP_ENV")
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def load_settings() -> AppSettings:
    """
    Явно загружает настройки приложения.
    """
    return AppSettings()
```

### app/presentation/api/v1/health.py

```
"""
Маршруты health endpoint.
"""

from fastapi import APIRouter, Depends

from app.container import Container
from app.presentation.api.dependencies.container import get_container
from app.presentation.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check(container: Container = Depends(get_container)) -> HealthResponse:
    settings = container.settings
    return HealthResponse(status="ok", environment=settings.environment)
```

### app/application/use_cases/get_message.py

```
"""
Use case получения сообщения.
"""

from app.application.dto.message_dto import MessageDTO
from app.domain.repositories.message_repository import MessageRepository


class GetMessageUseCase:
    def __init__(self, message_repository: MessageRepository) -> None:
        self._message_repository = message_repository

    def execute(self) -> MessageDTO:
        message = self._message_repository.get_message()
        return MessageDTO(text=message.text, source=message.source)
```
