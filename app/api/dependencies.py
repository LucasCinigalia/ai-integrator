"""Dependências FastAPI para injeção de dependência."""

from typing import Annotated

from fastapi import Depends

from app.services.item_service import ItemService, get_item_service

ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
