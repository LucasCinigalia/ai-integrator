"""Testes para o cliente HTTP da API externa."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.clients.api_client import ExternalAPIClient
from app.core.constants import HTTPHeaders


class TestExternalAPIClient:
    """Testes para a classe ExternalAPIClient."""

    @pytest.mark.asyncio
    async def test_client_context_manager(self):
        """Testa inicialização via context manager."""
        async with ExternalAPIClient() as client:
            assert client._client is not None
            assert isinstance(client._client, httpx.AsyncClient)

    @pytest.mark.asyncio
    async def test_get_data_success(self):
        """Testa requisição GET com sucesso."""
        mock_response_data = {"id": "1", "name": "Test Item"}

        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = MagicMock()
            mock_response.content = b'{"id": "1"}'
            mock_get.return_value = mock_response

            async with ExternalAPIClient() as client:
                result = await client.get_data("/items")

                assert result == mock_response_data
                mock_get.assert_called_once()
                call_kwargs = mock_get.call_args.kwargs
                assert HTTPHeaders.AUTHORIZATION in call_kwargs["headers"]
                assert call_kwargs["headers"][HTTPHeaders.AUTHORIZATION].startswith("Bearer ")

    @pytest.mark.asyncio
    async def test_get_data_with_params(self):
        """Testa requisição GET com query parameters."""
        mock_response_data = {"items": []}
        params = {"page": 1, "limit": 10}

        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = MagicMock()
            mock_response.content = b'{"items": []}'
            mock_get.return_value = mock_response

            async with ExternalAPIClient() as client:
                result = await client.get_data("/items", params=params)

                assert result == mock_response_data
                call_kwargs = mock_get.call_args.kwargs
                assert call_kwargs["params"] == params

    @pytest.mark.asyncio
    async def test_create_data_success(self):
        """Testa requisição POST com sucesso."""
        mock_data = {"name": "New Item", "description": "Test"}
        mock_response_data = {"id": "123", **mock_data}

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = MagicMock()
            mock_response.content = b'{"id": "123"}'
            mock_post.return_value = mock_response

            async with ExternalAPIClient() as client:
                result = await client.create_data("/items", mock_data)

                assert result == mock_response_data
                mock_post.assert_called_once()
                call_kwargs = mock_post.call_args.kwargs
                assert call_kwargs["json"] == mock_data
                assert HTTPHeaders.AUTHORIZATION in call_kwargs["headers"]

    @pytest.mark.asyncio
    async def test_update_data_success(self):
        """Testa requisição PUT com sucesso."""
        item_id = "123"
        mock_data = {"name": "Updated Item"}
        mock_response_data = {"id": item_id, **mock_data}

        with patch("httpx.AsyncClient.put") as mock_put:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = MagicMock()
            mock_response.content = b'{"id": "123"}'
            mock_put.return_value = mock_response

            async with ExternalAPIClient() as client:
                result = await client.update_data("/items", item_id, mock_data)

                assert result == mock_response_data
                mock_put.assert_called_once()
                call_args = mock_put.call_args
                assert f"/items/{item_id}" in str(call_args)

    @pytest.mark.asyncio
    async def test_http_error_handling(self):
        """Testa tratamento de erro HTTP."""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Not Found", request=MagicMock(), response=mock_response
            )
            mock_get.return_value = mock_response

            async with ExternalAPIClient() as client:
                with pytest.raises(httpx.HTTPStatusError):
                    await client.get_data("/items/999")

    @pytest.mark.asyncio
    async def test_client_not_initialized_error(self):
        """Testa erro quando cliente não é inicializado via context manager."""
        client = ExternalAPIClient()

        with pytest.raises(ValueError) as exc_info:
            await client.get_data("/items")

        assert "Cliente não inicializado" in str(exc_info.value)
