# Arquitetura - API Integrator

## Visão Geral

API Integrator segue **Clean Architecture** com separação clara de responsabilidades em 5 camadas principais. O fluxo de dados é unidirecional, das camadas externas (API) para as camadas internas (Core), respeitando o princípio de inversão de dependências.

## Diagrama de Camadas

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                  │
│  - Endpoints REST                                       │
│  - Request/Response handling                            │
│  - Dependency injection                                 │
├─────────────────────────────────────────────────────────┤
│                   Services Layer                        │
│  - Lógica de negócio                                    │
│  - Orquestração de operações                            │
│  - Transformação de dados                               │
├─────────────────────────────────────────────────────────┤
│                   Clients Layer                         │
│  - Integração com APIs externas                         │
│  - HTTP client wrapper                                  │
│  - Retry logic (futuro)                                 │
├─────────────────────────────────────────────────────────┤
│                   Models Layer (Pydantic)               │
│  - Schemas de request/response                          │
│  - Validação de dados                                   │
│  - Serialização/deserialização                          │
├─────────────────────────────────────────────────────────┤
│                   Core Layer                            │
│  - Configurações (Settings)                             │
│  - Autenticação (JWT Manager)                           │
│  - Constantes                                           │
│  - Utilitários                                          │
└─────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

### Request Flow (Exemplo: GET /items)

```
1. Cliente HTTP → FastAPI Endpoint (app/api/routes/items.py)
                    ↓
2. Dependency Injection → ItemService (app/services/item_service.py)
                    ↓
3. Service → ExternalAPIClient (app/clients/api_client.py)
                    ↓
4. Client → JWT Manager (app/core/auth.py) [obtém token]
                    ↓
5. Client → API Externa (httpx request com token)
                    ↓
6. API Externa → Response
                    ↓
7. Client → Deserializa para Pydantic models
                    ↓
8. Service → Processa/transforma dados
                    ↓
9. Endpoint → Retorna ItemResponse ao cliente
```

## Detalhamento das Camadas

### 1. API Layer (`app/api/`)

**Responsabilidade**: Interface HTTP da aplicação.

**Componentes**:
- `routes/items.py`: Endpoints CRUD para items
- `dependencies.py`: Dependency injection (get_item_service)

**Características**:
- Usa FastAPI decorators (`@router.get`, `@router.post`, etc.)
- Validação automática via Pydantic
- Documentação automática (Swagger/ReDoc)
- Dependency injection para services

**Exemplo**:
```python
@router.get("/items", response_model=List[ItemResponse])
async def get_items(service: ItemService = Depends(get_item_service)):
    return await service.get_items()
```

---

### 2. Services Layer (`app/services/`)

**Responsabilidade**: Lógica de negócio e orquestração.

**Componentes**:
- `item_service.py`: Lógica de negócio para items

**Características**:
- Orquestra chamadas a múltiplos clients se necessário
- Transforma dados entre camadas
- Implementa regras de negócio
- Não conhece detalhes de HTTP (request/response)

**Exemplo**:
```python
class ItemService:
    async def get_items(self) -> List[ItemResponse]:
        # Lógica de negócio aqui
        # Pode chamar ExternalAPIClient, aplicar filtros, etc.
        return items
```

**Nota**: Atualmente usa dados mockados. Em produção, chamaria `ExternalAPIClient`.

---

### 3. Clients Layer (`app/clients/`)

**Responsabilidade**: Integração com sistemas externos.

**Componentes**:
- `api_client.py`: Cliente HTTP para API externa

**Características**:
- Usa httpx para requisições assíncronas
- Gerencia autenticação (injeta JWT token)
- Connection pooling
- Context manager para gerenciamento de recursos

**Exemplo**:
```python
async with ExternalAPIClient() as client:
    data = await client.get_data("/items")
```

**Funcionalidades**:
- ✅ Injeção automática de JWT token
- ✅ Timeout configurável
- ✅ Async/await
- 🔜 Retry logic (roadmap)
- 🔜 Circuit breaker (roadmap)

---

### 4. Models Layer (`app/models/`)

**Responsabilidade**: Definição de estruturas de dados.

**Componentes**:
- `schemas.py`: Schemas Pydantic para request/response

**Características**:
- Validação automática
- Type hints completos
- Serialização/deserialização JSON
- Geração de JSON Schema

**Schemas Principais**:
- `ItemBase`: Campos base de um item
- `ItemCreate`: Schema para criar item (POST)
- `ItemUpdate`: Schema para atualizar item (PUT)
- `ItemResponse`: Schema de resposta (GET)
- `HealthResponse`: Schema de health check

**Exemplo**:
```python
class ItemResponse(ItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
```

---

### 5. Core Layer (`app/core/`)

**Responsabilidade**: Funcionalidades core compartilhadas.

**Componentes**:
- `config.py`: Configurações via Pydantic Settings
- `auth.py`: Gerenciamento de JWT tokens
- `constants.py`: Constantes da aplicação

**Características**:

#### config.py
- Carrega variáveis de .env
- Validação de configurações
- Singleton pattern (lru_cache)
- Type safety

#### auth.py
- `JWTManager`: Gerencia ciclo de vida de tokens
- Cache de token em memória
- Verificação de expiração
- Renovação automática

#### constants.py
- Constantes compartilhadas
- Evita magic numbers/strings
- Centraliza valores reutilizados

---

## Padrões de Design

### 1. Dependency Injection

**Onde**: API Layer → Services Layer

**Como**: FastAPI `Depends()`

**Benefícios**:
- Facilita testes (mock de dependências)
- Desacopla camadas
- Gerenciamento automático de ciclo de vida

**Exemplo**:
```python
def get_item_service() -> ItemService:
    return ItemService()

@router.get("/items")
async def get_items(service: ItemService = Depends(get_item_service)):
    return await service.get_items()
```

---

### 2. Repository Pattern (Implícito)

**Onde**: Services Layer ↔ Clients Layer

**Como**: Services chamam Clients para acesso a dados

**Benefícios**:
- Abstrai fonte de dados
- Facilita substituição de implementação
- Testes mais fáceis

---

### 3. Singleton Pattern

**Onde**: Core Layer (Settings, JWTManager)

**Como**: `@lru_cache` decorator

**Benefícios**:
- Uma única instância
- Performance (evita recarregar .env)
- Estado compartilhado

**Exemplo**:
```python
@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

### 4. Context Manager Pattern

**Onde**: Clients Layer (ExternalAPIClient)

**Como**: `async with` statement

**Benefícios**:
- Gerenciamento automático de recursos
- Cleanup garantido (connection close)
- Código mais limpo

**Exemplo**:
```python
async with ExternalAPIClient() as client:
    data = await client.get_data("/items")
# Connection fechada automaticamente
```

---

## Princípios Aplicados

### SOLID

| Princípio | Aplicação |
|-----------|-----------|
| **S**ingle Responsibility | Cada camada tem responsabilidade única |
| **O**pen/Closed | Extensível via dependency injection |
| **L**iskov Substitution | Services podem ser substituídos sem quebrar API |
| **I**nterface Segregation | Interfaces pequenas e focadas |
| **D**ependency Inversion | Camadas externas dependem de abstrações |

### Clean Architecture

- ✅ Independência de frameworks
- ✅ Testável (cada camada isoladamente)
- ✅ Independência de UI
- ✅ Independência de banco de dados
- ✅ Independência de agentes externos

### 12-Factor App

| Fator | Implementação |
|-------|---------------|
| **I. Codebase** | Git repository único |
| **II. Dependencies** | requirements.txt explícito |
| **III. Config** | .env (não hardcoded) |
| **IV. Backing services** | API externa como attached resource |
| **V. Build, release, run** | Separação clara (futuro: Docker) |
| **XI. Logs** | Logging estruturado para stdout |
| **XII. Admin processes** | Scripts separados (futuro) |

---

## Fluxo de Autenticação

```
1. Aplicação inicia → JWTManager criado (singleton)
                        ↓
2. ExternalAPIClient precisa fazer request
                        ↓
3. Client chama jwt_manager.get_token()
                        ↓
4. JWTManager verifica se token existe e é válido
                        ↓
5a. Token válido → retorna token do cache
5b. Token inválido/expirado → gera novo token
                        ↓
6. Client injeta token no header Authorization
                        ↓
7. Request enviado para API externa
```

---

## Tratamento de Erros

### Estratégia Atual

```
API Externa (erro) → ExternalAPIClient (httpx.HTTPStatusError)
                        ↓
                   Service (propaga exceção)
                        ↓
                   Endpoint (FastAPI exception handler)
                        ↓
                   Cliente (JSON error response)
```

### Exceções Customizadas (Futuro)

```python
# app/core/exceptions.py (futuro)
class APIIntegratorException(Exception): ...
class ExternalAPIError(APIIntegratorException): ...
class AuthenticationError(APIIntegratorException): ...
class RateLimitError(APIIntegratorException): ...
```

---

## Escalabilidade

### Horizontal Scaling

- ✅ Stateless (exceto JWT cache em memória)
- ✅ Async/await (alta concorrência)
- 🔜 Redis para cache compartilhado (v0.3.0)
- 🔜 Load balancer ready (v0.5.0)

### Vertical Scaling

- ✅ Connection pooling (httpx)
- ✅ Async I/O (não bloqueia threads)
- 🔜 Database connection pooling (quando adicionar DB)

---

## Segurança

### Implementado

- ✅ JWT tokens (não expõe credenciais)
- ✅ Secrets via .env (não hardcoded)
- ✅ CORS configurável
- ✅ Validação de input (Pydantic)

### Roadmap

- 🔜 HTTPS enforcement (v0.6.0)
- 🔜 Rate limiting (v0.2.0)
- 🔜 Security headers (v0.6.0)
- 🔜 Secrets scanning (v0.6.0)

---

## Observabilidade

### Implementado

- ✅ Logging estruturado
- ✅ Health check endpoint
- ✅ Documentação automática (Swagger/ReDoc)

### Roadmap

- 🔜 Métricas (Prometheus) (v0.4.0)
- 🔜 Distributed tracing (v0.4.0)
- 🔜 Structured logging (JSON) (v0.4.0)

---

## Decisões Arquiteturais

Ver [PROJECT.md](../project/PROJECT.md) e [STATE.md](../project/STATE.md) para decisões detalhadas.

---

## Diagramas

### Estrutura de Diretórios

```
app/
├── core/              # Core Layer
│   ├── __init__.py
│   ├── config.py      # Settings (Pydantic)
│   ├── auth.py        # JWT Manager
│   └── constants.py   # Constantes
├── models/            # Models Layer
│   ├── __init__.py
│   └── schemas.py     # Pydantic schemas
├── clients/           # Clients Layer
│   ├── __init__.py
│   └── api_client.py  # HTTP client
├── services/          # Services Layer
│   ├── __init__.py
│   └── item_service.py
└── api/               # API Layer
    ├── __init__.py
    ├── dependencies.py
    └── routes/
        ├── __init__.py
        └── items.py   # Endpoints
```

### Dependências entre Módulos

```
main.py
  ↓
app/api/routes/items.py
  ↓
app/api/dependencies.py
  ↓
app/services/item_service.py
  ↓
app/clients/api_client.py
  ↓
app/core/auth.py
  ↓
app/core/config.py

app/models/schemas.py (usado por todas as camadas)
```

---

## Testes

### Estratégia de Testes por Camada

| Camada | Tipo de Teste | Foco |
|--------|---------------|------|
| **API** | Integration | Request/response, status codes |
| **Services** | Unit | Lógica de negócio |
| **Clients** | Unit + Integration | HTTP calls, error handling |
| **Models** | Unit | Validação Pydantic |
| **Core** | Unit | Config loading, JWT generation |

### Estrutura de Testes

```
tests/
├── conftest.py           # Fixtures compartilhadas
├── test_auth.py          # Testa app/core/auth.py
├── test_client.py        # Testa app/clients/api_client.py
└── test_endpoints.py     # Testa app/api/routes/items.py
```

---

## Referências

- [Clean Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [12-Factor App](https://12factor.net/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
