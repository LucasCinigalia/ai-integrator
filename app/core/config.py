"""Configurações da aplicação usando Pydantic Settings."""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente.

    Usa Pydantic Settings para validação e carregamento automático do .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    api_base_url: str = Field(
        default="https://api.example.com", description="URL base da API externa"
    )
    api_timeout: int = Field(default=30, description="Timeout para requisições HTTP em segundos")

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
