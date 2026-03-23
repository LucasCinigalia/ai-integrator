"""Exceções customizadas da aplicação."""


class APIIntegratorException(Exception):
    """Exceção base da aplicação."""

    pass


class ExternalAPIError(APIIntegratorException):
    """Erro ao comunicar com API externa."""

    def __init__(self, status_code: int, message: str) -> None:
        """
        Inicializa exceção de erro da API externa.

        Args:
            status_code: Código HTTP de status
            message: Mensagem de erro
        """
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")


class ExternalAPITimeout(APIIntegratorException):
    """Timeout na comunicação com API externa."""

    pass


class ExternalAPIUnavailable(APIIntegratorException):
    """API externa indisponível (circuit breaker aberto)."""

    pass


class ItemNotFoundError(APIIntegratorException):
    """Item não encontrado."""

    pass
