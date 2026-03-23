"""Service layer para RD Station Conversas API."""

import logging
from datetime import datetime
from typing import Any, Dict

from app.clients.rd_conversas_client import RDConversasClient
from app.models.rd_conversas_schemas import (
    MessageContent,
    MessageHistoryParams,
    MessageHistoryResponse,
)

logger = logging.getLogger(__name__)


def _map_api_message_to_content(msg: Dict[str, Any], index: int) -> MessageContent:
    """Mapeia mensagem da API Tallos para MessageContent."""
    msg_id = msg.get("id") or msg.get("_id") or f"msg_{index}"
    contact = msg.get("contact") or {}
    contact_phone = (
        msg.get("contact_phone")
        or msg.get("recipient_number")
        or contact.get("phone")
        or msg.get("from")
        or msg.get("to")
        or ""
    )
    message_text = msg.get("message") or msg.get("content") or ""
    ts = msg.get("timestamp") or msg.get("created_at")
    if ts is None:
        timestamp = datetime.now()
    elif isinstance(ts, datetime):
        timestamp = ts
    else:
        ts_str = str(ts).replace("Z", "+00:00")
        timestamp = datetime.fromisoformat(ts_str)
    sent_by = msg.get("sent_by", "")
    direction = (
        "outbound"
        if sent_by in ("operator", "bot")
        else "inbound"
    )
    return MessageContent(
        id=str(msg_id),
        contact_phone=str(contact_phone),
        message=str(message_text),
        encrypted_message=msg.get("encrypted_message"),
        timestamp=timestamp,
        direction=direction,
        status=msg.get("status"),
    )


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
            _map_api_message_to_content(msg, i)
            for i, msg in enumerate(raw_data.get("messages", []))
        ]

        return MessageHistoryResponse(
            messages=messages,
            total=raw_data.get("total", 0),
            limit=raw_data.get("limit", params.limit),
            offset=raw_data.get("offset", params.offset),
        )
