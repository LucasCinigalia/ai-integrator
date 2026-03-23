"""Dependências FastAPI para injeção de dependência."""

from typing import Annotated

from fastapi import Depends

from app.clients.api_client import ExternalAPIClient
from app.clients.rd_conversas_client import RDConversasClient
from app.services.item_service import ItemService
from app.services.rd_conversas_service import RDConversasService


def get_rd_conversas_service() -> RDConversasService:
    """
    Retorna instância do RDConversasService.

    Returns:
        RDConversasService: Instância do serviço RD Conversas
    """
    client = RDConversasClient()
    return RDConversasService(client)


def get_item_service() -> ItemService:
    """
    Retorna instância do ItemService com cliente da API externa.

    Returns:
        ItemService: Instância do serviço
    """
    client = ExternalAPIClient()
    return ItemService(client=client)


ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
