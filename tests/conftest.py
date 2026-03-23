"""Configuração e fixtures do pytest."""

from datetime import datetime, timezone
from typing import AsyncGenerator, List

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.models.schemas import ItemResponse
from app.services.item_service import ItemService
from main import app


@pytest.fixture
def test_client() -> TestClient:
    """
    Fixture que retorna um TestClient do FastAPI.

    Returns:
        TestClient: Cliente de teste para a aplicação
    """
    return TestClient(app)


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


@pytest.fixture
def mock_item_service(sample_items: List[ItemResponse]) -> ItemService:
    """
    Fixture que retorna um ItemService mockado.

    Args:
        sample_items: Items de exemplo

    Returns:
        ItemService: Serviço mockado com dados de teste
    """
    service = ItemService()
    service._items = sample_items.copy()
    return service
