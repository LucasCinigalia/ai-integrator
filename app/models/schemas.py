"""Schemas Pydantic para validação de dados."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ItemBase(BaseModel):
    """Schema base para Item com campos comuns."""

    name: str = Field(..., min_length=1, max_length=100, description="Nome do item")
    description: Optional[str] = Field(None, max_length=500, description="Descrição do item")


class ItemCreate(ItemBase):
    """Schema para criação de Item via POST."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "Item Exemplo", "description": "Descrição do item exemplo"}
        }
    )


class ItemUpdate(BaseModel):
    """
    Schema para atualização de Item via PUT.

    Todos os campos são opcionais para permitir atualização parcial.
    """

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nome do item")
    description: Optional[str] = Field(None, max_length=500, description="Descrição do item")

    model_config = ConfigDict(
        json_schema_extra={"example": {"name": "Item Atualizado", "description": "Nova descrição"}}
    )


class ItemResponse(ItemBase):
    """Schema para resposta de Item."""

    id: str = Field(..., description="ID único do item")
    created_at: datetime = Field(..., description="Data e hora de criação")
    updated_at: Optional[datetime] = Field(None, description="Data e hora da última atualização")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Item Exemplo",
                "description": "Descrição do item exemplo",
                "created_at": "2024-03-22T10:30:00Z",
                "updated_at": "2024-03-22T11:00:00Z",
            }
        },
    )


class TokenResponse(BaseModel):
    """Schema para resposta de token JWT."""

    access_token: str = Field(..., description="Token JWT de acesso")
    token_type: str = Field(default="bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
            }
        }
    )


class ErrorResponse(BaseModel):
    """Schema para resposta de erro."""

    error: str = Field(..., description="Mensagem de erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais do erro")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "Item não encontrado",
                "detail": "O item com ID especificado não existe",
            }
        }
    )


class HealthResponse(BaseModel):
    """Schema para resposta do health check."""

    status: str = Field(default="healthy", description="Status da aplicação")
    version: str = Field(..., description="Versão da aplicação")
    timestamp: datetime = Field(..., description="Timestamp da verificação")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "version": "0.1.0",
                "timestamp": "2024-03-22T10:30:00Z",
            }
        }
    )
