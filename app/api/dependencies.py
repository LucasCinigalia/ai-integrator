"""Dependências FastAPI para injeção de dependência."""

from typing import Annotated

from fastapi import Depends

from app.clients.api_client import ExternalAPIClient
from app.services.item_service import ItemService


def get_item_service() -> ItemService:
    """
    Retorna instância do ItemService com cliente da API externa.

    Returns:
        ItemService: Instância do serviço
    """
    client = ExternalAPIClient()
    return ItemService(client=client)


ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
