"""Módulo de descriptografia JWE para RD Station Conversas."""

import json
import logging
from typing import Union

from jose import jwe, jwk

logger = logging.getLogger(__name__)


class MessageDecryptor:
    """Descriptografador de mensagens JWE usando RSA-OAEP-256 + A256GCM com chaves JWK."""

    def __init__(self, private_key_jwk: str) -> None:
        """
        Inicializa descriptografador com chave privada em formato JWK.

        Args:
            private_key_jwk: Chave privada em formato JWK (JSON string)

        Raises:
            ValueError: Se a chave JWK for inválida
        """
        try:
            jwk_dict = json.loads(private_key_jwk)

            required_fields = ["kty", "n", "e", "d"]
            missing_fields = [f for f in required_fields if f not in jwk_dict]
            if missing_fields:
                raise ValueError(f"Campos obrigatórios ausentes no JWK: {missing_fields}")

            # jwe.decrypt espera JWK dict ou str, não o objeto de jwk.construct()
            self.private_key = jwk_dict

            logger.info("Chave privada JWK carregada com sucesso")

        except json.JSONDecodeError as e:
            logger.error("Erro ao parsear JWK JSON: %s", e)
            raise ValueError("Chave JWK inválida: JSON malformado") from e
        except ValueError:
            raise
        except Exception as e:
            logger.error("Erro ao carregar chave JWK: %s", e)
            raise ValueError(f"Falha ao carregar chave JWK: {e}") from e

    def decrypt_message(self, encrypted_jwe: str) -> Union[str, dict]:
        """
        Descriptografa mensagem JWE.

        Args:
            encrypted_jwe: Mensagem criptografada em formato JWE (compact serialization)

        Returns:
            Mensagem descriptografada (string ou dict se for JSON).

        Raises:
            ValueError: Se falhar na descriptografia
        """
        try:
            decrypted_bytes = jwe.decrypt(encrypted_jwe, self.private_key)
            try:
                decrypted_str = decrypted_bytes.decode("utf-8")
            except UnicodeDecodeError:
                decrypted_str = decrypted_bytes.decode("latin-1")

            try:
                return json.loads(decrypted_str)
            except json.JSONDecodeError:
                return decrypted_str

        except Exception as e:
            logger.error("Erro ao descriptografar mensagem JWE: %s", e)
            raise ValueError(f"Falha na descriptografia de mensagem: {e}") from e
