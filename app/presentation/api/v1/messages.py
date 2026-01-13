"""
Маршруты для сообщений.
"""

from fastapi import APIRouter, Depends

from app.application.use_cases.get_message import GetMessageUseCase
from app.container import Container
from app.presentation.api.dependencies.container import get_container
from app.presentation.schemas.message import MessageResponse

router = APIRouter()


def provide_use_case(container: Container = Depends(get_container)) -> GetMessageUseCase:
    return container.get_message_use_case


@router.get("/message", response_model=MessageResponse)
def get_message(use_case: GetMessageUseCase = Depends(provide_use_case)) -> MessageResponse:
    message_dto = use_case.execute()
    return MessageResponse(text=message_dto.text, source=message_dto.source)
