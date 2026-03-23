# Estrutura do Projeto - API Integrator

## Visão Geral

```
ai-integrator/
├── .git/                    # Controle de versão Git
├── .specs/                  # Especificações e documentação de projeto
│   ├── project/             # Documentos de projeto
│   ├── codebase/            # Análise de codebase (este arquivo)
│   ├── features/            # Especificações de features
│   └── quick/               # Tasks rápidas
├── app/                     # Código fonte da aplicação
│   ├── core/                # Core layer (config, auth, constants)
│   ├── models/              # Models layer (Pydantic schemas)
│   ├── clients/             # Clients layer (HTTP clients)
│   ├── services/            # Services layer (lógica de negócio)
│   └── api/                 # API layer (FastAPI endpoints)
├── tests/                   # Testes automatizados
├── docs/                    # Documentação técnica
├── references/              # Referências e guias
├── main.py                  # Entry point da aplicação
├── requirements.txt         # Dependências Python
├── pyproject.toml           # Configuração do projeto
├── .env                     # Variáveis de ambiente (não versionado)
├── .env.example             # Template de variáveis de ambiente
├── .gitignore               # Arquivos ignorados pelo Git
├── README.md                # Documentação principal
├── CONTRIBUTING.md          # Guia de contribuição
└── DOCS_STANDARD.md         # Padrão de documentação
```

---

## Detalhamento de Diretórios

### `.specs/` - Especificações do Projeto

Documentação estruturada seguindo tlc-spec-driven.

```
.specs/
├── project/
│   ├── PROJECT.md           # Visão, objetivos, princípios
│   ├── ROADMAP.md           # Features planejadas, milestones
│   └── STATE.md             # Estado atual, decisões, TODOs
├── codebase/
│   ├── STACK.md             # Stack tecnológica
│   ├── ARCHITECTURE.md      # Arquitetura detalhada
│   ├── CONVENTIONS.md       # Convenções de código
│   ├── STRUCTURE.md         # Este arquivo
│   ├── TESTING.md           # Estratégia de testes
│   ├── INTEGRATIONS.md      # Integrações externas
│   └── CONCERNS.md          # Tech debt, riscos
├── features/
│   └── [feature-name]/
│       ├── spec.md          # Especificação da feature
│       ├── context.md       # Decisões de design
│       ├── design.md        # Arquitetura da feature
│       └── tasks.md         # Tasks atômicas
└── quick/
    └── [NNN-slug]/
        ├── TASK.md          # Descrição da task
        └── SUMMARY.md       # Resumo da execução
```

**Propósito**: Manter histórico de decisões, especificações e estado do projeto.

---

### `app/` - Código Fonte

Código da aplicação organizado em camadas (Clean Architecture).

#### `app/core/` - Core Layer

```
app/core/
├── __init__.py
├── config.py                # Settings com Pydantic
├── auth.py                  # JWT Manager
└── constants.py             # Constantes da aplicação
```

**Responsabilidade**: Funcionalidades core compartilhadas por toda aplicação.

**Arquivos principais**:
- `config.py`: Carrega configurações do .env usando Pydantic Settings
- `auth.py`: Gerencia ciclo de vida de tokens JWT (geração, validação, cache)
- `constants.py`: Constantes compartilhadas (evita magic numbers/strings)

---

#### `app/models/` - Models Layer

```
app/models/
├── __init__.py
└── schemas.py               # Pydantic schemas
```

**Responsabilidade**: Definição de estruturas de dados e validação.

**Schemas principais**:
- `ItemBase`: Campos base de um item
- `ItemCreate`: Schema para criar item (POST)
- `ItemUpdate`: Schema para atualizar item (PUT)
- `ItemResponse`: Schema de resposta (GET)
- `HealthResponse`: Schema de health check

---

#### `app/clients/` - Clients Layer

```
app/clients/
├── __init__.py
└── api_client.py            # Cliente HTTP para API externa
```

**Responsabilidade**: Integração com sistemas externos (APIs, DBs).

**Classes principais**:
- `ExternalAPIClient`: Cliente HTTP assíncrono com httpx
  - Gerencia conexões (connection pooling)
  - Injeta JWT token automaticamente
  - Context manager para cleanup de recursos

---

#### `app/services/` - Services Layer

```
app/services/
├── __init__.py
└── item_service.py          # Lógica de negócio para items
```

**Responsabilidade**: Lógica de negócio e orquestração.

**Classes principais**:
- `ItemService`: Orquestra operações CRUD de items
  - Atualmente usa dados mockados
  - Futuro: integrará com `ExternalAPIClient`

---

#### `app/api/` - API Layer

```
app/api/
├── __init__.py
├── dependencies.py          # Dependency injection
└── routes/
    ├── __init__.py
    └── items.py             # Endpoints CRUD de items
```

**Responsabilidade**: Interface HTTP da aplicação (endpoints REST).

**Arquivos principais**:
- `dependencies.py`: Funções de dependency injection (ex: `get_item_service`)
- `routes/items.py`: Endpoints CRUD para items
  - GET /items - Listar items
  - GET /items/{id} - Buscar item por ID
  - POST /items - Criar item
  - PUT /items/{id} - Atualizar item
  - DELETE /items/{id} - Deletar item

---

### `tests/` - Testes

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartilhadas
├── test_auth.py             # Testes de autenticação (JWT)
├── test_client.py           # Testes de cliente HTTP
└── test_endpoints.py        # Testes de endpoints (integration)
```

**Estrutura**: Espelha estrutura de `app/` para facilitar localização.

**Cobertura atual**: ~70%  
**Meta**: >80%

---

### `docs/` - Documentação Técnica

```
docs/
├── index.md                 # Índice da documentação
├── sidebar.json             # Navegação (futuro)
├── installation.md          # Guia de instalação
├── api.md                   # Documentação de endpoints
└── architecture.md          # Arquitetura e decisões
```

**Propósito**: Documentação técnica detalhada para desenvolvedores.

---

### `references/` - Referências e Guias

```
references/
└── style-guide.md           # Guia de estilo para documentação
```

**Propósito**: Guias de referência (estilo, padrões, etc.).

---

## Arquivos Raiz

### `main.py` - Entry Point

**Propósito**: Ponto de entrada da aplicação.

**Conteúdo**:
- Configuração do FastAPI app
- Middleware (CORS)
- Lifecycle management (startup/shutdown)
- Inclusão de routers
- Endpoints globais (/, /health)
- Exception handlers
- Função main para rodar com uvicorn

---

### `requirements.txt` - Dependências

**Propósito**: Lista de dependências Python.

**Dependências principais**:
- fastapi>=0.110.0
- httpx>=0.27.0
- pydantic>=2.6.0
- pydantic-settings>=2.2.0
- python-jose[cryptography]>=3.3.0
- uvicorn[standard]>=0.27.0
- pytest>=8.1.0
- pytest-asyncio>=0.23.0

**Instalação**:
```bash
pip install -r requirements.txt
```

---

### `pyproject.toml` - Configuração do Projeto

**Propósito**: Configuração centralizada do projeto.

**Seções**:
- `[project]`: Metadados (nome, versão, dependências)
- `[tool.pytest.ini_options]`: Configuração do pytest
- `[tool.ruff]`: Configuração do linter/formatter

---

### `.env` e `.env.example`

**`.env`** (não versionado):
```env
API_BASE_URL=https://api.example.com
API_TIMEOUT=30
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
TOKEN_EXPIRY_MINUTES=30
APP_NAME=API Integrator
APP_VERSION=0.1.0
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

**`.env.example`** (versionado):
- Template de variáveis de ambiente
- Sem valores sensíveis
- Documentação de cada variável

---

### `.gitignore`

**Propósito**: Arquivos/diretórios ignorados pelo Git.

**Principais exclusões**:
- `__pycache__/`, `*.pyc` (bytecode Python)
- `.env` (secrets)
- `venv/`, `.venv/` (ambiente virtual)
- `.pytest_cache/` (cache de testes)
- `*.log` (logs)

---

### `README.md`

**Propósito**: Documentação principal do projeto.

**Seções**:
- Descrição e features
- Arquitetura (diagrama)
- Tecnologias
- Instalação
- Como rodar
- Testes
- Endpoints disponíveis
- Autenticação
- Próximos passos
- Decisões arquiteturais

---

### `CONTRIBUTING.md`

**Propósito**: Guia para contribuidores.

**Conteúdo**:
- Processo de contribuição para documentação (docs-writer)
- Convenção de commits
- Como fazer fork e PR

---

### `DOCS_STANDARD.md`

**Propósito**: Padrão de documentação do projeto.

**Conteúdo**:
- Fluxo do docs-writer (4 passos)
- Estrutura da documentação
- Princípios obrigatórios
- Checklist antes de commitar

---

## Fluxo de Arquivos

### Request Flow

```
Cliente HTTP
    ↓
main.py (FastAPI app)
    ↓
app/api/routes/items.py (Endpoint)
    ↓
app/api/dependencies.py (DI)
    ↓
app/services/item_service.py (Lógica de negócio)
    ↓
app/clients/api_client.py (HTTP client)
    ↓
app/core/auth.py (JWT Manager)
    ↓
API Externa
```

### Configuration Flow

```
.env (variáveis de ambiente)
    ↓
app/core/config.py (Pydantic Settings)
    ↓
settings (singleton)
    ↓
Usado por toda aplicação
```

### Test Flow

```
pytest (test runner)
    ↓
tests/conftest.py (fixtures)
    ↓
tests/test_*.py (test files)
    ↓
app/* (código testado)
```

---

## Padrões de Organização

### Princípio de Responsabilidade Única

Cada arquivo/módulo tem responsabilidade única e bem definida.

**Exemplo**:
- `config.py`: Apenas configurações
- `auth.py`: Apenas autenticação JWT
- `api_client.py`: Apenas cliente HTTP

### Separação de Camadas

Camadas não pulam níveis:
- ✅ API → Services → Clients
- ❌ API → Clients (pula Services)

### Imports Absolutos

```python
# ✅ Bom
from app.core.config import settings
from app.models.schemas import ItemResponse

# ❌ Evitar
from ..core.config import settings
```

### Testes Espelham Estrutura

```
app/core/auth.py → tests/test_auth.py
app/clients/api_client.py → tests/test_client.py
app/api/routes/items.py → tests/test_endpoints.py
```

---

## Crescimento do Projeto

### Adicionar Nova Feature

1. Criar spec em `.specs/features/[feature-name]/`
2. Adicionar models em `app/models/schemas.py`
3. Criar service em `app/services/[feature]_service.py`
4. Criar endpoints em `app/api/routes/[feature].py`
5. Adicionar testes em `tests/test_[feature].py`
6. Atualizar documentação

### Adicionar Nova Integração

1. Criar client em `app/clients/[integration]_client.py`
2. Adicionar configurações em `app/core/config.py`
3. Documentar em `.specs/codebase/INTEGRATIONS.md`
4. Adicionar testes em `tests/test_[integration]_client.py`

### Adicionar Novo Endpoint

1. Definir schemas em `app/models/schemas.py`
2. Implementar em `app/api/routes/[resource].py`
3. Adicionar dependency em `app/api/dependencies.py` se necessário
4. Adicionar testes em `tests/test_endpoints.py`
5. Atualizar `docs/api.md`

---

## Arquivos Gerados (Não Versionados)

```
__pycache__/                 # Bytecode Python
*.pyc                        # Bytecode compilado
.pytest_cache/               # Cache do pytest
.ruff_cache/                 # Cache do ruff
*.log                        # Logs
.env                         # Secrets
venv/, .venv/                # Ambiente virtual
*.egg-info/                  # Metadados de instalação
dist/, build/                # Build artifacts
```

---

## Métricas

| Métrica | Valor Atual |
|---------|-------------|
| **Total de arquivos Python** | 21 |
| **Total de arquivos de teste** | 4 |
| **Linhas de código (app/)** | ~1500 |
| **Linhas de teste** | ~300 |
| **Cobertura de testes** | ~70% |
| **Arquivos de documentação** | 8 |

---

## Referências

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Package Structure](https://docs.python-guide.org/writing/structure/)
- [FastAPI Project Structure](https://fastapi.tiangolo.com/tutorial/)
