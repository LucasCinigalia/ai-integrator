"""Cliente HTTP para comunicação com API externa."""

import logging
from typing import Any, Dict, Optional

import httpx
from pybreaker import CircuitBreaker
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.auth import jwt_manager
from app.core.config import settings
from app.core.constants import ContentTypes, ErrorMessages, HTTPHeaders
from app.core.exceptions import (
    ExternalAPIError,
    ExternalAPITimeout,
    ExternalAPIUnavailable,
)

logger = logging.getLogger(__name__)


class ExternalAPIClient:
    """
    Cliente HTTP assíncrono para consumir API externa.

    Gerencia automaticamente:
    - Injeção de token JWT nos headers
    - Timeout de requisições
    - Tratamento de erros HTTP
    - Lifecycle do httpx.AsyncClient via context manager
    """

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None) -> None:
        """
        Inicializa o cliente da API externa.

        Args:
            base_url: URL base da API (usa settings se não fornecido)
            timeout: Timeout em segundos (usa settings se não fornecido)
        """
        self.base_url = base_url or settings.api_base_url
        self.timeout = timeout or settings.api_timeout
        self._client: Optional[httpx.AsyncClient] = None
        self._circuit_breaker = CircuitBreaker(
            fail_max=5, reset_timeout=60, name="ExternalAPICircuitBreaker"
        )

    async def __aenter__(self) -> "ExternalAPIClient":
        """Inicializa o cliente HTTP ao entrar no context manager."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={
                HTTPHeaders.CONTENT_TYPE: ContentTypes.JSON,
                HTTPHeaders.ACCEPT: ContentTypes.JSON,
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha o cliente HTTP ao sair do context manager."""
        if self._client:
            await self._client.aclose()

    def _get_auth_headers(self) -> Dict[str, str]:
        """
        Obtém headers de autenticação com token JWT.

        Returns:
            Dict[str, str]: Headers com token de autorização
        """
        token = jwt_manager.get_current_token()
        return {HTTPHeaders.AUTHORIZATION: f"Bearer {token}"}

    async def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """
        Processa resposta HTTP e trata erros.

        Args:
            response: Resposta HTTP do httpx

        Returns:
            Dict[str, Any]: Dados JSON da resposta

        Raises:
            ExternalAPIError: Se a resposta indicar erro HTTP
        """
        try:
            response.raise_for_status()
            return response.json() if response.content else {}
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise ExternalAPIError(e.response.status_code, e.response.text)
        except Exception as e:
            logger.error(f"Error processing response: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True,
    )
    async def get_data(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Realiza requisição GET para a API externa.

        Args:
            endpoint: Endpoint da API (ex: "/items")
            params: Query parameters opcionais

        Returns:
            Dict[str, Any]: Dados retornados pela API

        Raises:
            ValueError: Se o cliente não foi inicializado
            ExternalAPIError: Se a requisição falhar
            ExternalAPITimeout: Se houver timeout
            ExternalAPIUnavailable: Se circuit breaker estiver aberto
        """
        if not self._client:
            raise ValueError("Cliente não inicializado. Use 'async with ExternalAPIClient()'")

        headers = self._get_auth_headers()

        try:
            logger.info(f"GET request to {endpoint}")
            response = await self._client.get(endpoint, headers=headers, params=params)
            return await self._handle_response(response)
        except httpx.TimeoutException as e:
            logger.error(f"API timeout: {endpoint}")
            raise ExternalAPITimeout(f"Timeout ao acessar {endpoint}")
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {endpoint}")
            raise ExternalAPIError(503, f"Falha ao conectar: {str(e)}")
        except ExternalAPIError:
            raise
        except Exception as e:
            logger.error(f"GET request failed: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True,
    )
    async def create_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza requisição POST para criar dados na API externa.

        Args:
            endpoint: Endpoint da API (ex: "/items")
            data: Dados a serem enviados no body

        Returns:
            Dict[str, Any]: Dados retornados pela API

        Raises:
            ValueError: Se o cliente não foi inicializado
            ExternalAPIError: Se a requisição falhar
            ExternalAPITimeout: Se houver timeout
        """
        if not self._client:
            raise ValueError("Cliente não inicializado. Use 'async with ExternalAPIClient()'")

        headers = self._get_auth_headers()

        try:
            logger.info(f"POST request to {endpoint}")
            response = await self._client.post(endpoint, headers=headers, json=data)
            return await self._handle_response(response)
        except httpx.TimeoutException as e:
            logger.error(f"API timeout: {endpoint}")
            raise ExternalAPITimeout(f"Timeout ao acessar {endpoint}")
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {endpoint}")
            raise ExternalAPIError(503, f"Falha ao conectar: {str(e)}")
        except ExternalAPIError:
            raise
        except Exception as e:
            logger.error(f"POST request failed: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True,
    )
    async def update_data(
        self, endpoint: str, item_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Realiza requisição PUT para atualizar dados na API externa.

        Args:
            endpoint: Endpoint base da API (ex: "/items")
            item_id: ID do item a ser atualizado
            data: Dados a serem atualizados

        Returns:
            Dict[str, Any]: Dados retornados pela API

        Raises:
            ValueError: Se o cliente não foi inicializado
            ExternalAPIError: Se a requisição falhar
            ExternalAPITimeout: Se houver timeout
        """
        if not self._client:
            raise ValueError("Cliente não inicializado. Use 'async with ExternalAPIClient()'")

        headers = self._get_auth_headers()
        full_endpoint = f"{endpoint}/{item_id}"

        try:
            logger.info(f"PUT request to {full_endpoint}")
            response = await self._client.put(full_endpoint, headers=headers, json=data)
            return await self._handle_response(response)
        except httpx.TimeoutException as e:
            logger.error(f"API timeout: {full_endpoint}")
            raise ExternalAPITimeout(f"Timeout ao acessar {full_endpoint}")
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {full_endpoint}")
            raise ExternalAPIError(503, f"Falha ao conectar: {str(e)}")
        except ExternalAPIError:
            raise
        except Exception as e:
            logger.error(f"PUT request failed: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True,
    )
    async def delete_data(self, endpoint: str, item_id: str) -> Dict[str, Any]:
        """
        Realiza requisição DELETE para remover dados na API externa.

        Args:
            endpoint: Endpoint base da API (ex: "/items")
            item_id: ID do item a ser removido

        Returns:
            Dict[str, Any]: Dados retornados pela API

        Raises:
            ValueError: Se o cliente não foi inicializado
            ExternalAPIError: Se a requisição falhar
            ExternalAPITimeout: Se houver timeout
        """
        if not self._client:
            raise ValueError("Cliente não inicializado. Use 'async with ExternalAPIClient()'")

        headers = self._get_auth_headers()
        full_endpoint = f"{endpoint}/{item_id}"

        try:
            logger.info(f"DELETE request to {full_endpoint}")
            response = await self._client.delete(full_endpoint, headers=headers)
            return await self._handle_response(response)
        except httpx.TimeoutException as e:
            logger.error(f"API timeout: {full_endpoint}")
            raise ExternalAPITimeout(f"Timeout ao acessar {full_endpoint}")
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {full_endpoint}")
            raise ExternalAPIError(503, f"Falha ao conectar: {str(e)}")
        except ExternalAPIError:
            raise
        except Exception as e:
            logger.error(f"DELETE request failed: {str(e)}")
            raise
