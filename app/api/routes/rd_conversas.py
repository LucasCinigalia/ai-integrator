"""Endpoints da API para RD Station Conversas."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_rd_conversas_service
from app.models.rd_conversas_schemas import (
    MessageHistoryParams,
    MessageHistoryResponse,
)
from app.services.rd_conversas_service import RDConversasService

router = APIRouter(prefix="/rd-conversas", tags=["RD Conversas"])


@router.get(
    "/messages/history",
    response_model=MessageHistoryResponse,
    summary="Listar histórico de mensagens",
    description="Retorna histórico de conversas do RD Station Conversas com mensagens descriptografadas",
)
async def get_messages_history(
    limit: int = Query(default=50, ge=1, le=100, description="Número de mensagens"),
    offset: int = Query(default=0, ge=0, description="Offset para paginação"),
    contact_phone: Optional[str] = Query(
        default=None, description="Filtrar por telefone"
    ),
    start_date: Optional[datetime] = Query(
        default=None, description="Data inicial"
    ),
    end_date: Optional[datetime] = Query(default=None, description="Data final"),
    service: RDConversasService = Depends(get_rd_conversas_service),
) -> MessageHistoryResponse:
    """Endpoint para buscar histórico de mensagens."""
    if start_date is None:
        start_date = datetime.now(timezone.utc) - timedelta(days=30)

    params = MessageHistoryParams(
        limit=limit,
        offset=offset,
        contact_phone=contact_phone,
        start_date=start_date,
        end_date=end_date,
    )

    return await service.get_messages_history(params)
