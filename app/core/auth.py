"""Gerenciamento de autenticação JWT."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt

from app.core.config import settings
from app.core.constants import ErrorMessages


class JWTManager:
    """
    Gerenciador de tokens JWT.

    Responsável por gerar, validar e gerenciar tokens JWT para autenticação
    com a API externa.
    """

    def __init__(self) -> None:
        """Inicializa o gerenciador JWT com as configurações."""
        self.secret_key = settings.jwt_secret
        self.algorithm = settings.jwt_algorithm
        self.expiry_minutes = settings.token_expiry_minutes
        self._current_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

    def generate_token(
        self, data: Optional[Dict[str, Any]] = None, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Gera um novo token JWT.

        Args:
            data: Dados adicionais para incluir no payload do token
            expires_delta: Tempo customizado de expiração (opcional)

        Returns:
            str: Token JWT codificado
        """
        to_encode = data.copy() if data else {}

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.expiry_minutes)

        to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc), "type": "access"})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Valida e decodifica um token JWT.

        Args:
            token: Token JWT para validar

        Returns:
            Dict[str, Any]: Payload decodificado do token

        Raises:
            ValueError: Se o token for inválido ou expirado
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            raise ValueError(f"{ErrorMessages.INVALID_TOKEN}: {str(e)}")

    def is_token_expired(self, token: str) -> bool:
        """
        Verifica se um token está expirado.

        Args:
            token: Token JWT para verificar

        Returns:
            bool: True se expirado, False caso contrário
        """
        try:
            payload = self.validate_token(token)
            exp_timestamp = payload.get("exp")
            if not exp_timestamp:
                return True

            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            return datetime.now(timezone.utc) >= exp_datetime
        except ValueError:
            return True

    def get_current_token(self) -> str:
        """
        Retorna um token válido, gerando um novo se necessário.

        Implementa cache de token: reutiliza o token atual se ainda válido,
        ou gera um novo se expirado ou inexistente.

        Returns:
            str: Token JWT válido
        """
        if self._current_token and not self.is_token_expired(self._current_token):
            return self._current_token

        mock_data = {"sub": "api-integrator", "service": "external-api"}

        self._current_token = self.generate_token(mock_data)
        self._token_expiry = datetime.now(timezone.utc) + timedelta(minutes=self.expiry_minutes)

        return self._current_token

    def clear_token(self) -> None:
        """Limpa o token em cache, forçando geração de um novo na próxima chamada."""
        self._current_token = None
        self._token_expiry = None


jwt_manager = JWTManager()
