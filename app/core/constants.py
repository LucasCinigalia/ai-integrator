"""Constantes da aplicação."""

from enum import Enum


class HTTPStatus(int, Enum):
    """HTTP Status Codes mais utilizados."""

    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class ErrorMessages:
    """Mensagens de erro padrão."""

    ITEM_NOT_FOUND = "Item não encontrado"
    INVALID_TOKEN = "Token inválido ou expirado"
    AUTHENTICATION_FAILED = "Falha na autenticação"
    EXTERNAL_API_ERROR = "Erro ao comunicar com API externa"
    VALIDATION_ERROR = "Erro de validação nos dados"
    INTERNAL_ERROR = "Erro interno do servidor"


class HTTPHeaders:
    """Headers HTTP comuns."""

    AUTHORIZATION = "Authorization"
    CONTENT_TYPE = "Content-Type"
    ACCEPT = "Accept"


class ContentTypes:
    """Content Types comuns."""

    JSON = "application/json"
    FORM = "application/x-www-form-urlencoded"


HTTP_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 1
