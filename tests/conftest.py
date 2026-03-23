"""Configuração e fixtures do pytest."""

from datetime import datetime, timezone
from typing import AsyncGenerator, List
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.api.dependencies import get_item_service
from app.clients.api_client import ExternalAPIClient
from app.models.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.services.item_service import ItemService
from main import app


class MockItemService:
    """Mock do ItemService para testes de endpoints."""

    def __init__(self):
        """Inicializa o mock com dados de exemplo."""
        now = datetime.now(timezone.utc)
        self._items = [
            ItemResponse(
                id="test-id-001",
                name="Test Item 1",
                description="Test description 1",
                created_at=now,
                updated_at=now,
            ),
            ItemResponse(
                id="test-id-002",
                name="Test Item 2",
                description="Test description 2",
                created_at=now,
                updated_at=None,
            ),
        ]

    async def get_items(self) -> List[ItemResponse]:
        """Retorna lista de items mockados."""
        return self._items

    async def get_item_by_id(self, item_id: str) -> ItemResponse | None:
        """Busca item por ID."""
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    async def create_item(self, item_data: ItemCreate) -> ItemResponse:
        """Cria novo item."""
        now = datetime.now(timezone.utc)
        new_item = ItemResponse(
            id="new-test-id",
            name=item_data.name,
            description=item_data.description,
            created_at=now,
            updated_at=now,
        )
        self._items.append(new_item)
        return new_item

    async def update_item(self, item_id: str, item_data: ItemUpdate) -> ItemResponse:
        """Atualiza item existente."""
        for idx, item in enumerate(self._items):
            if item.id == item_id:
                update_data = item_data.model_dump(exclude_unset=True)
                updated_item = item.model_copy(
                    update={**update_data, "updated_at": datetime.now(timezone.utc)}
                )
                self._items[idx] = updated_item
                return updated_item
        raise ValueError("Item not found")

    async def delete_item(self, item_id: str) -> bool:
        """Remove item."""
        for idx, item in enumerate(self._items):
            if item.id == item_id:
                self._items.pop(idx)
                return True
        raise ValueError("Item not found")


@pytest.fixture
def test_client() -> TestClient:
    """
    Fixture que retorna um TestClient do FastAPI com service mockado.

    Returns:
        TestClient: Cliente de teste para a aplicação
    """

    def get_mock_service():
        return MockItemService()

    app.dependency_overrides[get_item_service] = get_mock_service
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture que retorna um AsyncClient para testes assíncronos.

    Yields:
        AsyncClient: Cliente HTTP assíncrono
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def sample_items() -> List[ItemResponse]:
    """
    Fixture com items de exemplo para testes.

    Returns:
        List[ItemResponse]: Lista de items mockados
    """
    now = datetime.now(timezone.utc)

    return [
        ItemResponse(
            id="test-id-001",
            name="Test Item 1",
            description="Test description 1",
            created_at=now,
            updated_at=now,
        ),
        ItemResponse(
            id="test-id-002",
            name="Test Item 2",
            description="Test description 2",
            created_at=now,
            updated_at=None,
        ),
    ]
