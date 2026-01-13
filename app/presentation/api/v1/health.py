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
