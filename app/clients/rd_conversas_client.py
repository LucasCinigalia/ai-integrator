"""Cliente HTTP para API RD Station Conversas v2."""

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import httpx
from jose import jwt

from app.core.config import settings
from app.core.crypto import MessageDecryptor

logger = logging.getLogger(__name__)


class RDConversasClient:
    """Cliente HTTP para API RD Station Conversas v2 (Tallos)."""

    def __init__(self) -> None:
        """Inicializa cliente com URL base correta e Bearer Token."""
        self.base_url = settings.api_base_url
        self.bearer_token = settings.api_token

        if not self.bearer_token:
            raise ValueError(
                "Bearer token não configurado (API_TOKEN no .env)"
            )

        self.customer_id = self._extract_customer_id_from_token()
        logger.info(
            "RDConversasClient inicializado com customer_id: %s",
            self.customer_id or "NENHUM",
        )

        private_key_jwk = settings.rd_conversas_private_key_jwk
        self.decryptor = (
            MessageDecryptor(private_key_jwk)
            if private_key_jwk
            else None
        )

        if not self.decryptor:
            logger.warning(
                "Descriptografia desabilitada: chave JWK não encontrada"
            )

        self.timeout = settings.api_timeout

    def _extract_customer_id_from_token(self) -> Optional[str]:
        """
        Extrai customer_id (company) do JWT.

        Returns:
            Optional[str]: ID da empresa ou None se não encontrado
        """
        logger.info("Iniciando extração de customer_id do JWT...")
        try:
            payload = jwt.decode(
                self.bearer_token,
                key="",
                options={"verify_signature": False}
            )
            logger.info("JWT decodificado com sucesso. Payload keys: %s", list(payload.keys()))
            customer_id = payload.get("company")
            if customer_id:
                logger.info("Customer ID extraído do JWT: %s", customer_id)
                return customer_id
            else:
                logger.warning(
                    "Campo 'company' não encontrado no JWT payload: %s",
                    payload
                )
                return None
        except Exception as e:
            logger.error("Erro ao decodificar JWT: %s", e, exc_info=True)
            return None

    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers com Bearer Token."""
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def get_messages_history(
        self,
        limit: int = 50,
        offset: int = 0,
        contact_phone: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Busca histórico de mensagens.

        Endpoint: GET https://api.tallos.com.br/v2/messages/history
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            headers = self._get_headers()

            # API Tallos usa page (1-based) e limit, não offset
            page = (offset // limit) + 1 if limit > 0 else 1
            params: Dict[str, Any] = {"limit": limit, "page": page}

            if self.customer_id:
                params["customer_id"] = self.customer_id
            if contact_phone:
                params["contact_phone"] = contact_phone
            if start_date:
                params["start_date"] = start_date.strftime("%Y-%m-%d")
            if end_date:
                params["end_date"] = end_date.strftime("%Y-%m-%d")

            response = await client.get(
                f"{self.base_url}/messages/history",
                headers=headers,
                params=params,
            )

            if response.status_code >= 400:
                try:
                    body = response.text
                    logger.error(
                        "API Tallos retornou %s: %s",
                        response.status_code,
                        body[:500] if len(body) > 500 else body,
                    )
                except Exception:
                    pass
                response.raise_for_status()

            data = response.json()

            if self.decryptor and "messages" in data:
                for message in data["messages"]:
                    if "encrypted_message" in message:
                        try:
                            decrypted = self.decryptor.decrypt_message(
                                message["encrypted_message"]
                            )
                            message["message"] = (
                                decrypted
                                if isinstance(decrypted, str)
                                else json.dumps(decrypted)
                            )
                        except ValueError as e:
                            msg_id = message.get("id", "?")
                            logger.warning(
                                "Falha ao descriptografar mensagem %s: %s",
                                msg_id,
                                e,
                            )
                            message["message"] = "[ERRO NA DESCRIPTOGRAFIA]"

            return data
