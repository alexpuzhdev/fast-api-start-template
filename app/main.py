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
