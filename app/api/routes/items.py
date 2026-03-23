"""Endpoints da API para gerenciamento de Items."""

import logging
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import ItemServiceDep
from app.core.constants import ErrorMessages, HTTPStatus
from app.models.schemas import ErrorResponse, ItemCreate, ItemResponse, ItemUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/items", tags=["items"])


@router.get(
    "",
    response_model=List[ItemResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista todos os items",
    description="Retorna lista completa de items cadastrados no sistema",
)
async def get_items(service: ItemServiceDep) -> List[ItemResponse]:
    """
    Endpoint para listar todos os items.

    Returns:
        List[ItemResponse]: Lista de items
    """
    try:
        items = await service.get_items()
        return items
    except Exception as e:
        logger.error(f"Error retrieving items: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ErrorMessages.INTERNAL_ERROR
        )


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Busca item por ID",
    description="Retorna um item específico baseado no ID fornecido",
    responses={404: {"model": ErrorResponse, "description": "Item não encontrado"}},
)
async def get_item(item_id: str, service: ItemServiceDep) -> ItemResponse:
    """
    Endpoint para buscar um item específico por ID.

    Args:
        item_id: ID do item a ser buscado
        service: Serviço de items injetado

    Returns:
        ItemResponse: Item encontrado

    Raises:
        HTTPException: 404 se item não for encontrado
    """
    try:
        item = await service.get_item_by_id(item_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessages.ITEM_NOT_FOUND
            )

        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving item {item_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ErrorMessages.INTERNAL_ERROR
        )


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria novo item",
    description="Cria um novo item no sistema com os dados fornecidos",
    responses={400: {"model": ErrorResponse, "description": "Dados inválidos"}},
)
async def create_item(item_data: ItemCreate, service: ItemServiceDep) -> ItemResponse:
    """
    Endpoint para criar um novo item.

    Args:
        item_data: Dados do item a ser criado
        service: Serviço de items injetado

    Returns:
        ItemResponse: Item criado com ID e timestamps
    """
    try:
        new_item = await service.create_item(item_data)
        return new_item
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ErrorMessages.INTERNAL_ERROR
        )


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualiza item existente",
    description="Atualiza os dados de um item existente baseado no ID",
    responses={
        404: {"model": ErrorResponse, "description": "Item não encontrado"},
        400: {"model": ErrorResponse, "description": "Dados inválidos"},
    },
)
async def update_item(item_id: str, item_data: ItemUpdate, service: ItemServiceDep) -> ItemResponse:
    """
    Endpoint para atualizar um item existente.

    Args:
        item_id: ID do item a ser atualizado
        item_data: Dados para atualização
        service: Serviço de items injetado

    Returns:
        ItemResponse: Item atualizado

    Raises:
        HTTPException: 404 se item não for encontrado
    """
    try:
        updated_item = await service.update_item(item_id, item_data)
        return updated_item
    except ValueError as e:
        if ErrorMessages.ITEM_NOT_FOUND in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessages.ITEM_NOT_FOUND
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating item {item_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ErrorMessages.INTERNAL_ERROR
        )


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove item",
    description="Remove um item do sistema baseado no ID",
    responses={404: {"model": ErrorResponse, "description": "Item não encontrado"}},
)
async def delete_item(item_id: str, service: ItemServiceDep) -> None:
    """
    Endpoint para remover um item.

    Args:
        item_id: ID do item a ser removido
        service: Serviço de items injetado

    Raises:
        HTTPException: 404 se item não for encontrado
    """
    try:
        await service.delete_item(item_id)
    except ValueError as e:
        if ErrorMessages.ITEM_NOT_FOUND in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=ErrorMessages.ITEM_NOT_FOUND
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting item {item_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ErrorMessages.INTERNAL_ERROR
        )
