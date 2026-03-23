"""Testes para o ItemService."""

from unittest.mock import AsyncMock

import pytest

from app.clients.api_client import ExternalAPIClient
from app.core.exceptions import ExternalAPIError, ExternalAPITimeout
from app.models.schemas import ItemCreate, ItemUpdate
from app.services.item_service import ItemService


class TestItemService:
    """Testes para ItemService com API mockada."""

    @pytest.mark.asyncio
    async def test_get_items(self):
        """Testa get_items com API mockada."""
        mock_client = AsyncMock(spec=ExternalAPIClient)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_data = AsyncMock(
            return_value=[
                {
                    "id": "123",
                    "name": "Test Item",
                    "description": "Test",
                    "created_at": "2024-03-22T10:00:00Z",
                    "updated_at": "2024-03-22T11:00:00Z",
                }
            ]
        )

        service = ItemService(client=mock_client)
        items = await service.get_items()

        assert len(items) == 1
        assert items[0].name == "Test Item"
        mock_client.get_data.assert_called_once_with("/items")

    @pytest.mark.asyncio
    async def test_get_item_by_id(self):
        """Testa get_item_by_id com API mockada."""
        mock_client = AsyncMock(spec=ExternalAPIClient)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_data = AsyncMock(
            return_value={
                "id": "123",
                "name": "Test Item",
                "description": "Test",
                "created_at": "2024-03-22T10:00:00Z",
                "updated_at": "2024-03-22T11:00:00Z",
            }
        )

        service = ItemService(client=mock_client)
        item = await service.get_item_by_id("123")

        assert item is not None
        assert item.name == "Test Item"
        mock_client.get_data.assert_called_once_with("/items/123")

    @pytest.mark.asyncio
    async def test_create_item(self):
        """Testa create_item com API mockada."""
        mock_client = AsyncMock(spec=ExternalAPIClient)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.create_data = AsyncMock(
            return_value={
                "id": "new-123",
                "name": "New Item",
                "description": "New description",
                "created_at": "2024-03-22T12:00:00Z",
                "updated_at": "2024-03-22T12:00:00Z",
            }
        )

        service = ItemService(client=mock_client)
        item_data = ItemCreate(name="New Item", description="New description")
        new_item = await service.create_item(item_data)

        assert new_item.name == "New Item"
        assert new_item.id == "new-123"
        mock_client.create_data.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_item(self):
        """Testa update_item com API mockada."""
        mock_client = AsyncMock(spec=ExternalAPIClient)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.update_data = AsyncMock(
            return_value={
                "id": "123",
                "name": "Updated Item",
                "description": "Updated description",
                "created_at": "2024-03-22T10:00:00Z",
                "updated_at": "2024-03-22T13:00:00Z",
            }
        )

        service = ItemService(client=mock_client)
        item_data = ItemUpdate(name="Updated Item", description="Updated description")
        updated_item = await service.update_item("123", item_data)

        assert updated_item.name == "Updated Item"
        mock_client.update_data.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_item(self):
        """Testa delete_item com API mockada."""
        mock_client = AsyncMock(spec=ExternalAPIClient)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.delete_data = AsyncMock(return_value={})

        service = ItemService(client=mock_client)
        result = await service.delete_item("123")

        assert result is True
        mock_client.delete_data.assert_called_once_with("/items", "123")

    @pytest.mark.asyncio
    async def test_get_items_handles_timeout(self):
        """Testa tratamento de timeout em get_items."""
        mock_client = AsyncMock(spec=ExternalAPIClient)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_data = AsyncMock(side_effect=ExternalAPITimeout("Timeout"))

        service = ItemService(client=mock_client)

        with pytest.raises(Exception) as exc_info:
            await service.get_items()

        assert "504" in str(exc_info.value) or "timeout" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_get_items_handles_api_error(self):
        """Testa tratamento de erro da API em get_items."""
        mock_client = AsyncMock(spec=ExternalAPIClient)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get_data = AsyncMock(side_effect=ExternalAPIError(500, "Internal error"))

        service = ItemService(client=mock_client)

        with pytest.raises(Exception) as exc_info:
            await service.get_items()

        assert "502" in str(exc_info.value) or "error" in str(exc_info.value).lower()
