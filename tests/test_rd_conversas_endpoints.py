"""Testes dos endpoints RD Station Conversas."""

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_rd_conversas_service
from app.models.rd_conversas_schemas import MessageContent, MessageHistoryResponse
from main import app


class MockRDConversasService:
    """Mock do RDConversasService para testes."""

    async def get_messages_history(self, params) -> MessageHistoryResponse:
        """Retorna histórico mockado."""
        return MessageHistoryResponse(
            messages=[
                MessageContent(
                    id="msg_001",
                    contact_phone="+5511999999999",
                    message="Test message",
                    encrypted_message=None,
                    timestamp=datetime.now(timezone.utc),
                    direction="inbound",
                    status="delivered",
                ),
            ],
            total=1,
            limit=params.limit,
            offset=params.offset,
        )


@pytest.fixture
def rd_conversas_test_client() -> TestClient:
    """Fixture com mock do RDConversasService."""
    app.dependency_overrides[get_rd_conversas_service] = lambda: MockRDConversasService()
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_rd_conversas_service, None)


def test_messages_history_endpoint(rd_conversas_test_client) -> None:
    """Testa endpoint de histórico."""
    response = rd_conversas_test_client.get("/api/v1/rd-conversas/messages/history")
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert "total" in data
    assert data["total"] == 1
    assert len(data["messages"]) == 1
    assert data["messages"][0]["message"] == "Test message"


def test_messages_history_endpoint_with_params(rd_conversas_test_client) -> None:
    """Testa endpoint com parâmetros de paginação."""
    response = rd_conversas_test_client.get(
        "/api/v1/rd-conversas/messages/history?limit=10&offset=0"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 10
    assert data["offset"] == 0
