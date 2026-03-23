"""Serviço de negócio para gerenciamento de Items."""

import logging
from typing import List, Optional

from fastapi import HTTPException, status

from app.clients.api_client import ExternalAPIClient
from app.core.constants import ErrorMessages
from app.core.exceptions import ExternalAPIError, ExternalAPITimeout
from app.models.schemas import ItemCreate, ItemResponse, ItemUpdate

logger = logging.getLogger(__name__)


class ItemService:
    """
    Serviço de lógica de negócio para Items.

    Integra com API externa para todas as operações.
    """

    def __init__(self, client: ExternalAPIClient) -> None:
        """
        Inicializa o serviço.

        Args:
            client: Cliente HTTP para API externa
        """
        self.client = client
        logger.info("ItemService initialized with API integration")

    async def get_items(self) -> List[ItemResponse]:
        """
        Retorna lista de todos os items da API externa.

        Returns:
            List[ItemResponse]: Lista de items
        """
        try:
            logger.info("Fetching items from external API")
            async with self.client as client:
                data = await client.get_data("/items")

                items = []
                items_data = data if isinstance(data, list) else data.get("items", [])

                for item_data in items_data:
                    items.append(
                        ItemResponse(
                            id=str(item_data.get("_id") or item_data.get("id")),
                            name=item_data["name"],
                            description=item_data.get("description"),
                            created_at=item_data.get("created_at") or item_data.get("createdAt"),
                            updated_at=item_data.get("updated_at") or item_data.get("updatedAt"),
                        )
                    )

                logger.info(f"Retrieved {len(items)} items from API")
                return items

        except ExternalAPITimeout:
            logger.error("Timeout fetching items from API")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="External API timeout"
            )
        except ExternalAPIError as e:
            logger.error(f"API error: {e.status_code}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"External API error: {e.message}",
            )

    async def get_item_by_id(self, item_id: str) -> Optional[ItemResponse]:
        """
        Busca um item específico por ID na API externa.

        Args:
            item_id: ID do item a ser buscado

        Returns:
            Optional[ItemResponse]: Item encontrado ou None
        """
        try:
            logger.info(f"Fetching item {item_id} from external API")
            async with self.client as client:
                data = await client.get_data(f"/items/{item_id}")

                return ItemResponse(
                    id=str(data.get("_id") or data.get("id")),
                    name=data["name"],
                    description=data.get("description"),
                    created_at=data.get("created_at") or data.get("createdAt"),
                    updated_at=data.get("updated_at") or data.get("updatedAt"),
                )

        except ExternalAPIError as e:
            if e.status_code == 404:
                return None
            logger.error(f"API error: {e.status_code}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"External API error: {e.message}",
            )
        except ExternalAPITimeout:
            logger.error("Timeout fetching item from API")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="External API timeout"
            )

    async def create_item(self, item_data: ItemCreate) -> ItemResponse:
        """
        Cria um novo item na API externa.

        Args:
            item_data: Dados do item a ser criado

        Returns:
            ItemResponse: Item criado com ID e timestamps
        """
        try:
            logger.info("Creating item via external API")
            async with self.client as client:
                payload = item_data.model_dump()
                data = await client.create_data("/items", payload)

                return ItemResponse(
                    id=str(data.get("_id") or data.get("id")),
                    name=data["name"],
                    description=data.get("description"),
                    created_at=data.get("created_at") or data.get("createdAt"),
                    updated_at=data.get("updated_at") or data.get("updatedAt"),
                )

        except ExternalAPITimeout:
            logger.error("Timeout creating item via API")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="External API timeout"
            )
        except ExternalAPIError as e:
            logger.error(f"API error: {e.status_code}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"External API error: {e.message}",
            )

    async def update_item(self, item_id: str, item_data: ItemUpdate) -> ItemResponse:
        """
        Atualiza um item existente na API externa.

        Args:
            item_id: ID do item a ser atualizado
            item_data: Dados para atualização

        Returns:
            ItemResponse: Item atualizado

        Raises:
            ValueError: Se o item não for encontrado
        """
        try:
            logger.info(f"Updating item {item_id} via external API")
            async with self.client as client:
                payload = item_data.model_dump(exclude_unset=True)
                data = await client.update_data("/items", item_id, payload)

                return ItemResponse(
                    id=str(data.get("_id") or data.get("id")),
                    name=data["name"],
                    description=data.get("description"),
                    created_at=data.get("created_at") or data.get("createdAt"),
                    updated_at=data.get("updated_at") or data.get("updatedAt"),
                )

        except ExternalAPIError as e:
            if e.status_code == 404:
                logger.error(f"Item not found: {item_id}")
                raise ValueError(ErrorMessages.ITEM_NOT_FOUND)
            logger.error(f"API error: {e.status_code}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"External API error: {e.message}",
            )
        except ExternalAPITimeout:
            logger.error("Timeout updating item via API")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="External API timeout"
            )

    async def delete_item(self, item_id: str) -> bool:
        """
        Remove um item da API externa.

        Args:
            item_id: ID do item a ser removido

        Returns:
            bool: True se removido com sucesso

        Raises:
            ValueError: Se o item não for encontrado
        """
        try:
            logger.info(f"Deleting item {item_id} via external API")
            async with self.client as client:
                await client.delete_data("/items", item_id)
                logger.info(f"Item {item_id} deleted successfully")
                return True

        except ExternalAPIError as e:
            if e.status_code == 404:
                logger.error(f"Item not found: {item_id}")
                raise ValueError(ErrorMessages.ITEM_NOT_FOUND)
            logger.error(f"API error: {e.status_code}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"External API error: {e.message}",
            )
        except ExternalAPITimeout:
            logger.error("Timeout deleting item via API")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="External API timeout"
            )
