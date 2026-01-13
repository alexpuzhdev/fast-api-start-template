"""
Корневой роутер версии API.
"""

from fastapi import APIRouter

from app.presentation.api.v1.health import router as health_router
from app.presentation.api.v1.messages import router as message_router

router = APIRouter()
router.include_router(health_router)
router.include_router(message_router)
