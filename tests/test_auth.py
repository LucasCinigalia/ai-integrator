"""Testes para o módulo de autenticação JWT."""

from datetime import timedelta

import pytest
from jose import jwt

from app.core.auth import JWTManager
from app.core.config import settings


class TestJWTManager:
    """Testes para a classe JWTManager."""

    def test_generate_token_success(self):
        """Testa geração de token JWT com sucesso."""
        manager = JWTManager()
        data = {"sub": "test-user", "role": "admin"}

        token = manager.generate_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_generate_token_with_custom_expiry(self):
        """Testa geração de token com tempo de expiração customizado."""
        manager = JWTManager()
        data = {"sub": "test-user"}
        custom_expiry = timedelta(minutes=60)

        token = manager.generate_token(data, expires_delta=custom_expiry)

        assert token is not None
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        assert "exp" in payload
        assert "iat" in payload

    def test_validate_token_success(self):
        """Testa validação de token válido."""
        manager = JWTManager()
        data = {"sub": "test-user", "role": "admin"}
        token = manager.generate_token(data)

        payload = manager.validate_token(token)

        assert payload is not None
        assert payload["sub"] == "test-user"
        assert payload["role"] == "admin"
        assert "exp" in payload
        assert "iat" in payload
        assert payload["type"] == "access"

    def test_validate_token_invalid(self):
        """Testa validação de token inválido."""
        manager = JWTManager()
        invalid_token = "invalid.token.here"

        with pytest.raises(ValueError) as exc_info:
            manager.validate_token(invalid_token)

        assert "Token inválido ou expirado" in str(exc_info.value)

    def test_is_token_expired_valid(self):
        """Testa verificação de token não expirado."""
        manager = JWTManager()
        token = manager.generate_token({"sub": "test"})

        is_expired = manager.is_token_expired(token)

        assert is_expired is False

    def test_is_token_expired_with_expired_token(self):
        """Testa verificação de token expirado."""
        manager = JWTManager()
        expired_delta = timedelta(seconds=-10)
        token = manager.generate_token({"sub": "test"}, expires_delta=expired_delta)

        is_expired = manager.is_token_expired(token)

        assert is_expired is True

    def test_get_current_token_generates_new(self):
        """Testa que get_current_token gera novo token."""
        manager = JWTManager()

        token = manager.get_current_token()

        assert token is not None
        assert isinstance(token, str)
        payload = manager.validate_token(token)
        assert payload["sub"] == "api-integrator"
        assert payload["service"] == "external-api"

    def test_get_current_token_caches(self):
        """Testa que get_current_token reutiliza token válido."""
        manager = JWTManager()

        token1 = manager.get_current_token()
        token2 = manager.get_current_token()

        assert token1 == token2

    def test_clear_token(self):
        """Testa limpeza do token em cache."""
        manager = JWTManager()

        token1 = manager.get_current_token()
        assert manager._current_token is not None

        manager.clear_token()

        assert manager._current_token is None
        assert manager._token_expiry is None
