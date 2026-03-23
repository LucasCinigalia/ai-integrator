"""Configurações da aplicação usando Pydantic Settings."""

import logging
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente.

    Usa Pydantic Settings para validação e carregamento automático do .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    api_base_url: str = Field(
        default="https://api.tallos.com.br/v2", description="URL base da API RD Station Conversas (Tallos)"
    )
    api_timeout: int = Field(default=30, description="Timeout para requisições HTTP em segundos")
    api_token: Optional[str] = Field(
        default=None, description="Token JWT pré-configurado da API externa"
    )

    jwt_secret: str = Field(
        default="dev-secret-key-change-in-production",
        description="Chave secreta para assinar tokens JWT",
    )
    jwt_algorithm: str = Field(default="HS256", description="Algoritmo de criptografia JWT")
    token_expiry_minutes: int = Field(
        default=30, description="Tempo de expiração do token em minutos"
    )

    app_name: str = Field(default="API Integrator", description="Nome da aplicação")
    app_version: str = Field(default="0.1.0", description="Versão da aplicação")
    debug: bool = Field(default=False, description="Modo debug")

    host: str = Field(default="0.0.0.0", description="Host do servidor")
    port: int = Field(default=8000, description="Porta do servidor")

    rd_conversas_private_key_path: Optional[str] = Field(
        default="secrets/rd_conversas_private.jwk.json",
        description="Caminho para arquivo JWK com chave privada RSA para descriptografia (opcional)",
    )

    @property
    def rd_conversas_private_key_jwk(self) -> Optional[str]:
        """Carrega chave privada JWK do arquivo."""
        if not self.rd_conversas_private_key_path:
            return None

        key_path = Path(self.rd_conversas_private_key_path)
        if not key_path.exists():
            logger.warning(
                "Arquivo de chave privada não encontrado: %s", key_path
            )
            return None

        try:
            return key_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error("Erro ao ler chave privada: %s", e)
            return None


@lru_cache
def get_settings() -> Settings:
    """
    Retorna instância singleton das configurações.

    Usa lru_cache para garantir que apenas uma instância seja criada
    durante o ciclo de vida da aplicação.

    Returns:
        Settings: Instância das configurações
    """
    return Settings()


settings = get_settings()
