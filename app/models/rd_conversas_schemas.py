"""Schemas Pydantic para RD Station Conversas API."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class MessageHistoryParams(BaseModel):
    """Parâmetros para busca de histórico de mensagens."""

    limit: Optional[int] = Field(default=50, ge=1, le=100, description="Número de mensagens")
    offset: Optional[int] = Field(default=0, ge=0, description="Offset para paginação")
    contact_phone: Optional[str] = Field(None, description="Filtrar por telefone do contato")
    start_date: Optional[datetime] = Field(None, description="Data inicial do período")
    end_date: Optional[datetime] = Field(None, description="Data final do período")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "limit": 50,
                "offset": 0,
                "contact_phone": "+5511999999999",
                "start_date": "2026-03-01T00:00:00Z",
                "end_date": "2026-03-23T23:59:59Z",
            }
        }
    )


class MessageContent(BaseModel):
    """Conteúdo de uma mensagem."""

    id: str = Field(..., description="ID único da mensagem")
    contact_phone: str = Field(..., description="Telefone do contato")
    message: str = Field(..., description="Mensagem descriptografada")
    encrypted_message: Optional[str] = Field(None, description="Mensagem original criptografada (JWE)")
    timestamp: datetime = Field(..., description="Data e hora da mensagem")
    direction: str = Field(..., description="Direção: inbound ou outbound")
    status: Optional[str] = Field(None, description="Status da mensagem")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "msg_abc123",
                "contact_phone": "+5511999999999",
                "message": "Olá! Como posso ajudar?",
                "encrypted_message": None,
                "timestamp": "2026-03-23T10:30:00Z",
                "direction": "outbound",
                "status": "delivered",
            }
        }
    )


class MessageHistoryResponse(BaseModel):
    """Resposta do endpoint de histórico de mensagens."""

    messages: List[MessageContent] = Field(..., description="Lista de mensagens")
    total: int = Field(..., ge=0, description="Total de mensagens encontradas")
    limit: int = Field(..., ge=1, le=100, description="Limite aplicado na busca")
    offset: int = Field(..., ge=0, description="Offset aplicado na busca")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "messages": [],
                "total": 0,
                "limit": 50,
                "offset": 0,
            }
        }
    )
