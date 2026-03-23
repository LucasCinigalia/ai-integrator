# Integrações Externas - API Integrator

## Visão Geral

Este documento descreve todas as integrações com sistemas externos, incluindo APIs, bibliotecas e serviços.

---

## API Externa (Mock)

### Status

🔶 **Mockado** - Atualmente usa dados simulados. Integração real planejada.

### Descrição

API REST externa que será consumida pela aplicação. Atualmente mockada no `ItemService`.

### Configuração

**Variáveis de ambiente** (`.env`):
```env
API_BASE_URL=https://api.example.com
API_TIMEOUT=30
```

**Settings** (`app/core/config.py`):
```python
api_base_url: str = Field(default="https://api.example.com")
api_timeout: int = Field(default=30)
```

### Cliente HTTP

**Implementação**: `app/clients/api_client.py`

**Classe**: `ExternalAPIClient`

**Características**:
- Async/await (httpx)
- Connection pooling
- Timeout configurável
- Injeção automática de JWT token
- Context manager

**Exemplo de uso**:
```python
async with ExternalAPIClient() as client:
    data = await client.get_data("/items")
    created = await client.create_data("/items", {"name": "New Item"})
    updated = await client.update_data("/items/123", {"name": "Updated"})
```

### Autenticação

**Tipo**: JWT (JSON Web Token)

**Implementação**: `app/core/auth.py` (`JWTManager`)

**Fluxo**:
1. `JWTManager` gera token JWT
2. Token é cacheado em memória
3. Antes de cada request, verifica se token é válido
4. Se expirado, gera novo token automaticamente
5. Token é injetado no header `Authorization: Bearer <token>`

**Configuração**:
```env
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
TOKEN_EXPIRY_MINUTES=30
```

### Endpoints Consumidos (Planejado)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/items` | Listar items |
| GET | `/items/{id}` | Buscar item por ID |
| POST | `/items` | Criar item |
| PUT | `/items/{id}` | Atualizar item |
| DELETE | `/items/{id}` | Deletar item |

### Error Handling

**Erros tratados**:
- `httpx.TimeoutException`: Timeout na requisição
- `httpx.HTTPStatusError`: Erro HTTP (4xx, 5xx)
- `httpx.ConnectError`: Falha de conexão

**Exemplo**:
```python
try:
    data = await client.get_data("/items")
except httpx.TimeoutException:
    logger.error("API timeout")
    raise HTTPException(status_code=504, detail="External API timeout")
except httpx.HTTPStatusError as e:
    logger.error(f"API error: {e.response.status_code}")
    raise HTTPException(status_code=502, detail="External API error")
```

### Migração de Mock para Real

**Passos**:

1. Configurar `API_BASE_URL` no `.env` com URL real
2. Atualizar `ItemService` para usar `ExternalAPIClient`:

```python
# Antes (mock)
class ItemService:
    async def get_items(self) -> List[ItemResponse]:
        return MOCK_ITEMS

# Depois (real)
class ItemService:
    def __init__(self, client: ExternalAPIClient):
        self.client = client
    
    async def get_items(self) -> List[ItemResponse]:
        async with self.client as client:
            data = await client.get_data("/items")
            return [ItemResponse(**item) for item in data]
```

3. Atualizar dependency injection em `app/api/dependencies.py`:

```python
def get_item_service() -> ItemService:
    client = ExternalAPIClient()
    return ItemService(client=client)
```

4. Atualizar testes para mockar `ExternalAPIClient`

---

## Bibliotecas Principais

### FastAPI

**Versão**: 0.110+  
**Propósito**: Framework web  
**Documentação**: https://fastapi.tiangolo.com/

**Uso**:
- Definição de endpoints REST
- Validação automática (Pydantic)
- Documentação automática (Swagger/ReDoc)
- Dependency injection

**Exemplo**:
```python
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/items")
async def get_items(service: ItemService = Depends(get_item_service)):
    return await service.get_items()
```

---

### httpx

**Versão**: 0.27+  
**Propósito**: Cliente HTTP assíncrono  
**Documentação**: https://www.python-httpx.org/

**Uso**:
- Requisições HTTP assíncronas
- Connection pooling
- HTTP/2 support
- Timeout configurável

**Exemplo**:
```python
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com/items")
    data = response.json()
```

---

### Pydantic

**Versão**: 2.6+  
**Propósito**: Validação de dados  
**Documentação**: https://docs.pydantic.dev/

**Uso**:
- Schemas de request/response
- Validação automática
- Serialização/deserialização
- Settings management

**Exemplo**:
```python
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
```

---

### python-jose

**Versão**: 3.3+  
**Propósito**: JWT (JSON Web Tokens)  
**Documentação**: https://python-jose.readthedocs.io/

**Uso**:
- Geração de tokens JWT
- Validação de tokens
- Suporte a múltiplos algoritmos (HS256, RS256, etc.)

**Exemplo**:
```python
from jose import jwt

token = jwt.encode(payload, secret_key, algorithm="HS256")
decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
```

---

### uvicorn

**Versão**: 0.27+  
**Propósito**: Servidor ASGI  
**Documentação**: https://www.uvicorn.org/

**Uso**:
- Servidor HTTP para FastAPI
- Suporte a async/await
- Hot reload (desenvolvimento)
- Workers (produção)

**Exemplo**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

### pytest

**Versão**: 8.1+  
**Propósito**: Framework de testes  
**Documentação**: https://docs.pytest.org/

**Uso**:
- Testes unitários e de integração
- Fixtures
- Plugins (pytest-asyncio, pytest-cov)

**Exemplo**:
```python
@pytest.mark.asyncio
async def test_get_items(client):
    response = await client.get("/items")
    assert response.status_code == 200
```

---

## Integrações Futuras (Roadmap)

### Redis (v0.3.0)

**Propósito**: Cache de respostas da API externa

**Biblioteca**: `redis-py` ou `aioredis`

**Uso planejado**:
- Cache de GET requests
- TTL configurável por endpoint
- Invalidação de cache

**Exemplo**:
```python
# Futuro
async def get_items(self) -> List[ItemResponse]:
    cache_key = "items:all"
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    data = await self.client.get_data("/items")
    await redis.setex(cache_key, 300, json.dumps(data))
    return data
```

---

### Prometheus (v0.4.0)

**Propósito**: Métricas e monitoring

**Biblioteca**: `prometheus-client`

**Métricas planejadas**:
- Request count
- Request latency
- Error rate
- Active connections

**Exemplo**:
```python
# Futuro
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_latency = Histogram('http_request_duration_seconds', 'HTTP request latency')
```

---

### OpenTelemetry (v0.4.0)

**Propósito**: Distributed tracing

**Biblioteca**: `opentelemetry-api`, `opentelemetry-sdk`

**Uso planejado**:
- Trace requests através de toda aplicação
- Correlation IDs
- Exportação para Jaeger/Zipkin

---

### Docker (v0.5.0)

**Propósito**: Containerização

**Uso planejado**:
- Dockerfile multi-stage
- docker-compose para desenvolvimento
- Health checks

---

## Dependências de Desenvolvimento

### ruff

**Propósito**: Linter e formatter

**Uso**:
```bash
ruff format .
ruff check .
```

---

### pytest-asyncio

**Propósito**: Suporte a testes assíncronos

**Uso**:
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

---

### pytest-cov

**Propósito**: Cobertura de testes

**Uso**:
```bash
pytest --cov=app --cov-report=html
```

---

## Segurança

### Secrets Management

**Atual**: Variáveis de ambiente (`.env`)

**Futuro** (v0.6.0):
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault

### HTTPS

**Atual**: HTTP (desenvolvimento)

**Futuro** (v0.6.0):
- HTTPS enforcement
- Certificate management
- HSTS headers

---

## Monitoring e Observabilidade

### Logging

**Atual**: Python `logging` module

**Configuração**:
```python
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

**Futuro** (v0.4.0):
- Structured logging (JSON)
- Correlation IDs
- Log aggregation (ELK, Datadog)

---

### Health Checks

**Atual**: Endpoint `/health`

**Resposta**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-03-22T10:00:00Z"
}
```

**Futuro** (v0.4.0):
- Liveness probe
- Readiness probe
- Dependency health checks (API externa, Redis, DB)

---

## Rate Limiting (Futuro - v0.2.0)

**Biblioteca planejada**: `slowapi`

**Configuração planejada**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/items")
@limiter.limit("100/minute")
async def get_items():
    ...
```

---

## Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [httpx Documentation](https://www.python-httpx.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [python-jose Documentation](https://python-jose.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
