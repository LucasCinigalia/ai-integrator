"""Clients module - Integração com APIs externas."""

from app.clients.api_client import ExternalAPIClient
from app.clients.rd_conversas_client import RDConversasClient

__all__ = ["ExternalAPIClient", "RDConversasClient"]
