"""
API Integrator - Aplicação FastAPI para consumir API REST externa.

Este módulo é o ponto de entrada da aplicação.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import AsyncGenerator

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import items, rd_conversas
from app.core.config import settings
from app.core.metrics import metrics
from app.models.schemas import HealthResponse

logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Gerencia o ciclo de vida da aplicação.

    Executa código de inicialização no startup e limpeza no shutdown.
    """
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"API Base URL: {settings.api_base_url}")

    yield

    logger.info(f"Shutting down {settings.app_name}")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    API Integrator - Aplicação para consumir API REST externa com autenticação JWT.
    
    ## Características
    
    * **Clean Architecture**: Separação clara de responsabilidades
    * **Autenticação JWT**: Gerenciamento automático de tokens
    * **Async/Await**: Operações assíncronas para melhor performance
    * **Type Safety**: Validação completa com Pydantic
    * **Documentação Automática**: Swagger UI e ReDoc
    
    ## Endpoints Disponíveis
    
    * **Items**: CRUD completo para gerenciamento de items
    * **Health**: Verificação de saúde da aplicação
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
app.include_router(rd_conversas.router, prefix="/v1")


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Root endpoint",
    description="Retorna informações básicas da API",
)
async def root() -> dict:
    """
    Endpoint raiz da API.

    Returns:
        dict: Informações básicas da aplicação
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Verifica o status de saúde da aplicação",
)
async def health_check() -> HealthResponse:
    """
    Endpoint de health check.

    Returns:
        HealthResponse: Status da aplicação
    """
    return HealthResponse(
        status="healthy", version=settings.app_version, timestamp=datetime.now(timezone.utc)
    )


@app.get(
    "/metrics",
    status_code=status.HTTP_200_OK,
    summary="Application metrics",
    description="Retorna métricas de uso da aplicação",
)
async def get_metrics() -> dict:
    """
    Endpoint de métricas.

    Returns:
        dict: Estatísticas de uso da aplicação
    """
    return metrics.get_stats()


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception) -> JSONResponse:
    """
    Handler global para exceções não tratadas.

    Args:
        request: Request HTTP
        exc: Exceção capturada

    Returns:
        JSONResponse: Resposta de erro formatada
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning",
    )
