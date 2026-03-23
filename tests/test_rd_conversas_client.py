"""Testes do cliente HTTP RD Station Conversas."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.clients.rd_conversas_client import RDConversasClient


@pytest.mark.asyncio
async def test_client_initialization_with_token() -> None:
    """Testa inicialização do cliente com Bearer Token."""
    with patch("app.clients.rd_conversas_client.settings") as mock_settings:
        mock_settings.api_base_url = "https://api.tallos.com.br/v2"
        mock_settings.api_token = "test_token_123"
        mock_settings.rd_conversas_private_key_jwk = None
        mock_settings.api_timeout = 30

        client = RDConversasClient()
        assert client.bearer_token == "test_token_123"
        assert client.base_url == "https://api.tallos.com.br/v2"


@pytest.mark.asyncio
async def test_client_initialization_without_token() -> None:
    """Testa erro quando Bearer Token não está configurado."""
    with patch("app.clients.rd_conversas_client.settings") as mock_settings:
        mock_settings.api_token = None
        mock_settings.api_base_url = "https://api.tallos.com.br/v2"
        mock_settings.rd_conversas_private_key_jwk = None
        mock_settings.api_timeout = 30

        with pytest.raises(ValueError, match="Bearer token não configurado"):
            RDConversasClient()


@pytest.mark.asyncio
async def test_get_messages_history() -> None:
    """Testa busca de histórico com Bearer Token."""
    with patch("app.clients.rd_conversas_client.settings") as mock_settings:
        mock_settings.api_base_url = "https://api.tallos.com.br/v2"
        mock_settings.api_token = "test_token_123"
        mock_settings.rd_conversas_private_key_jwk = None
        mock_settings.api_timeout = 30

        client = RDConversasClient()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "messages": [],
            "total": 0,
            "limit": 50,
            "offset": 0,
        }
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_cls.return_value = mock_client

            result = await client.get_messages_history()

            assert result["total"] == 0
            assert "messages" in result
