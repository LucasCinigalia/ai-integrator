"""Serviço de negócio para gerenciamento de Items."""

import logging
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from app.core.constants import ErrorMessages
from app.models.schemas import ItemCreate, ItemResponse, ItemUpdate

logger = logging.getLogger(__name__)


class ItemService:
    """
    Serviço de lógica de negócio para Items.

    Implementação inicial com dados mockados em memória.
    Preparado para integração futura com ExternalAPIClient.
    """

    def __init__(self) -> None:
        """Inicializa o serviço com dados mockados."""
        self._items: List[ItemResponse] = self._create_mock_items()

    def _create_mock_items(self) -> List[ItemResponse]:
        """
        Cria lista de items mockados para demonstração.

        Returns:
            List[ItemResponse]: Lista de items de exemplo
        """
        now = datetime.now(timezone.utc)

        return [
            ItemResponse(
                id="550e8400-e29b-41d4-a716-446655440001",
                name="Notebook Dell",
                description="Notebook Dell Inspiron 15 com 16GB RAM",
                created_at=now,
                updated_at=now,
            ),
            ItemResponse(
                id="550e8400-e29b-41d4-a716-446655440002",
                name="Mouse Logitech",
                description="Mouse sem fio Logitech MX Master 3",
                created_at=now,
                updated_at=now,
            ),
            ItemResponse(
                id="550e8400-e29b-41d4-a716-446655440003",
                name="Teclado Mecânico",
                description="Teclado mecânico RGB com switches Cherry MX",
                created_at=now,
                updated_at=now,
            ),
            ItemResponse(
                id="550e8400-e29b-41d4-a716-446655440004",
                name="Monitor LG",
                description="Monitor LG UltraWide 34 polegadas",
                created_at=now,
                updated_at=now,
            ),
            ItemResponse(
                id="550e8400-e29b-41d4-a716-446655440005",
                name="Webcam Logitech",
                description="Webcam Full HD 1080p com microfone",
                created_at=now,
                updated_at=None,
            ),
        ]

    async def get_items(self) -> List[ItemResponse]:
        """
        Retorna lista de todos os items.

        Returns:
            List[ItemResponse]: Lista de items
        """
        logger.info(f"Retrieving {len(self._items)} items")
        return self._items

    async def get_item_by_id(self, item_id: str) -> Optional[ItemResponse]:
        """
        Busca um item específico por ID.

        Args:
            item_id: ID do item a ser buscado

        Returns:
            Optional[ItemResponse]: Item encontrado ou None
        """
        logger.info(f"Searching for item with ID: {item_id}")

        for item in self._items:
            if item.id == item_id:
                return item

        return None

    async def create_item(self, item_data: ItemCreate) -> ItemResponse:
        """
        Cria um novo item.

        Args:
            item_data: Dados do item a ser criado

        Returns:
            ItemResponse: Item criado com ID e timestamps
        """
        now = datetime.now(timezone.utc)

        new_item = ItemResponse(
            id=str(uuid4()),
            name=item_data.name,
            description=item_data.description,
            created_at=now,
            updated_at=now,
        )

        self._items.append(new_item)
        logger.info(f"Item created with ID: {new_item.id}")

        return new_item

    async def update_item(self, item_id: str, item_data: ItemUpdate) -> ItemResponse:
        """
        Atualiza um item existente.

        Args:
            item_id: ID do item a ser atualizado
            item_data: Dados para atualização

        Returns:
            ItemResponse: Item atualizado

        Raises:
            ValueError: Se o item não for encontrado
        """
        logger.info(f"Updating item with ID: {item_id}")

        for idx, item in enumerate(self._items):
            if item.id == item_id:
                update_data = item_data.model_dump(exclude_unset=True)

                if not update_data:
                    logger.warning(f"No fields to update for item {item_id}")
                    return item

                updated_item = item.model_copy(
                    update={**update_data, "updated_at": datetime.now(timezone.utc)}
                )

                self._items[idx] = updated_item
                logger.info(f"Item {item_id} updated successfully")

                return updated_item

        logger.error(f"Item not found: {item_id}")
        raise ValueError(ErrorMessages.ITEM_NOT_FOUND)

    async def delete_item(self, item_id: str) -> bool:
        """
        Remove um item.

        Args:
            item_id: ID do item a ser removido

        Returns:
            bool: True se removido com sucesso

        Raises:
            ValueError: Se o item não for encontrado
        """
        logger.info(f"Deleting item with ID: {item_id}")

        for idx, item in enumerate(self._items):
            if item.id == item_id:
                self._items.pop(idx)
                logger.info(f"Item {item_id} deleted successfully")
                return True

        logger.error(f"Item not found: {item_id}")
        raise ValueError(ErrorMessages.ITEM_NOT_FOUND)


_item_service_instance: Optional[ItemService] = None


def get_item_service() -> ItemService:
    """
    Retorna instância singleton do ItemService.

    Returns:
        ItemService: Instância do serviço
    """
    global _item_service_instance

    if _item_service_instance is None:
        _item_service_instance = ItemService()

    return _item_service_instance
