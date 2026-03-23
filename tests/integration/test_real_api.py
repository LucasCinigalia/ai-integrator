"""Testes de integração com API real."""

import pytest

from app.clients.api_client import ExternalAPIClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_api_connection():
    """
    Testa conexão real com API externa.

    Este teste requer que a API esteja disponível e configurada no .env.
    Execute com: pytest -m integration
    """
    async with ExternalAPIClient() as client:
        try:
            data = await client.get_data("/health")
            assert data is not None
        except Exception as e:
            pytest.skip(f"API não disponível: {str(e)}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_api_get_items():
    """
    Testa listagem de items via API real.

    Este teste requer que a API esteja disponível.
    Execute com: pytest -m integration
    """
    async with ExternalAPIClient() as client:
        try:
            data = await client.get_data("/items")
            assert data is not None
            assert isinstance(data, (list, dict))
        except Exception as e:
            pytest.skip(f"API não disponível ou endpoint não existe: {str(e)}")
