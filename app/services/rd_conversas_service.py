"""Service layer para RD Station Conversas API."""

import logging

from app.clients.rd_conversas_client import RDConversasClient
from app.models.rd_conversas_schemas import (
    MessageContent,
    MessageHistoryParams,
    MessageHistoryResponse,
)

logger = logging.getLogger(__name__)


class RDConversasService:
    """Service layer para RD Station Conversas."""

    def __init__(self, client: RDConversasClient) -> None:
        """Inicializa o service com cliente HTTP."""
        self.client = client

    async def get_messages_history(
        self, params: MessageHistoryParams
    ) -> MessageHistoryResponse:
        """
        Busca histórico de mensagens com validação e transformação.

        Args:
            params: Parâmetros de busca

        Returns:
            MessageHistoryResponse: Histórico formatado
        """
        raw_data = await self.client.get_messages_history(
            limit=params.limit,
            offset=params.offset,
            contact_phone=params.contact_phone,
            start_date=params.start_date,
            end_date=params.end_date,
        )

        messages = [
            MessageContent(**msg) for msg in raw_data.get("messages", [])
        ]

        return MessageHistoryResponse(
            messages=messages,
            total=raw_data.get("total", 0),
            limit=raw_data.get("limit", params.limit),
            offset=raw_data.get("offset", params.offset),
        )
