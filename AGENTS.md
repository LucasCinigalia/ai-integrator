# AGENTS.md - Regras e Padrões para Agentes de IA

Este documento define as regras, padrões e diretrizes que agentes de IA devem seguir ao trabalhar neste projeto.

**Prioridade**: 🔴 MÁXIMA - Este arquivo deve ser lido ANTES de qualquer modificação no projeto.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Convenções de Código](#convenções-de-código)
4. [Arquitetura e Design](#arquitetura-e-design)
5. [Documentação](#documentação)
6. [Testes](#testes)
7. [Workflow de Desenvolvimento](#workflow-de-desenvolvimento)
8. [Áreas Sensíveis](#áreas-sensíveis)
9. [Checklist de Modificações](#checklist-de-modificações)

---

## 🎯 Visão Geral

### Sobre o Projeto

**Nome**: API Integrator  
**Tipo**: Aplicação Python (FastAPI) para consumo de API REST externa  
**Arquitetura**: Clean Architecture (5 camadas)  
**Versão atual**: v0.1.0

### Princípios Fundamentais

1. **Clean Architecture**: Separação clara de responsabilidades
2. **Type Safety**: Type hints completos em todo código
3. **Async First**: Operações I/O sempre assíncronas
4. **Configuration as Code**: Sem hardcoding, tudo via .env
5. **Test-Driven**: Cobertura >80% (meta)
6. **Documentation First**: Código bem documentado

---

## 📁 Estrutura do Projeto

### Diretórios Principais

```
ai-integrator/
├── .specs/              # 🔴 CRÍTICO: Especificações do projeto
│   ├── project/         # Visão, roadmap, estado
│   ├── codebase/        # Análise técnica (stack, arquitetura, etc.)
│   ├── features/        # Specs de features
│   └── quick/           # Tasks rápidas
├── app/                 # Código fonte (5 camadas)
│   ├── core/            # Config, auth, constants
│   ├── models/          # Pydantic schemas
│   ├── clients/         # HTTP clients
│   ├── services/        # Lógica de negócio
│   └── api/             # FastAPI endpoints
├── tests/               # Testes (pytest)
├── docs/                # Documentação técnica
├── references/          # Guias de referência
└── main.py              # Entry point
```

### Documentos Obrigatórios a Ler

**ANTES de qualquer modificação**:

1. ✅ **AGENTS.md** (este arquivo)
2. ✅ **.specs/project/PROJECT.md** - Visão e objetivos
3. ✅ **.specs/project/STATE.md** - Estado atual, decisões, TODOs
4. ✅ **.specs/codebase/ARCHITECTURE.md** - Arquitetura detalhada
5. ✅ **.specs/codebase/CONVENTIONS.md** - Convenções de código

**Para features específicas**:

6. ✅ **.specs/project/ROADMAP.md** - Features planejadas
7. ✅ **.specs/codebase/CONCERNS.md** - Tech debt, áreas frágeis
8. ✅ **.specs/codebase/TESTING.md** - Estratégia de testes

---

## 💻 Convenções de Código

### Idioma

- **Código**: Inglês (variáveis, funções, classes)
- **Documentação**: Português (README, docs/, .specs/)
- **Docstrings**: Português
- **Commits**: Português

### Nomenclatura

```python
# ✅ Variáveis e funções: snake_case
user_id: UUID
def get_items() -> List[ItemResponse]: ...

# ✅ Classes: PascalCase
class ItemService: ...
class ExternalAPIClient: ...

# ✅ Constantes: UPPER_SNAKE_CASE
API_TIMEOUT = 30
MAX_RETRIES = 3

# ✅ Arquivos: snake_case
item_service.py
api_client.py
```

### Type Hints (OBRIGATÓRIO)

```python
# ✅ SEMPRE com type hints completos
def get_item(item_id: UUID) -> Optional[ItemResponse]:
    """Busca item por ID."""
    ...

async def create_item(data: ItemCreate) -> ItemResponse:
    """Cria novo item."""
    ...

# ❌ NUNCA sem type hints
def get_item(item_id):
    ...
```

### Imports

```python
# ✅ Ordem: stdlib → third-party → local
import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.config import settings
from app.models.schemas import ItemResponse

# ❌ Evitar imports relativos
from ..core.config import settings  # ❌
```

### Formatação

**Ferramenta**: `ruff`

```bash
# SEMPRE rodar antes de commit
ruff format .
ruff check .
```

**Configuração**: `pyproject.toml`
- Line length: 100 caracteres
- Target: Python 3.10+

---

## 🏗️ Arquitetura e Design

### Clean Architecture (5 Camadas)

```
API Layer (FastAPI)
    ↓ depende de
Services Layer (Lógica de negócio)
    ↓ depende de
Clients Layer (HTTP clients)
    ↓ depende de
Models Layer (Pydantic schemas)
    ↓ depende de
Core Layer (Config, Auth, Constants)
```

### Regras de Dependência

1. ✅ **Camadas superiores dependem de inferiores**
2. ❌ **NUNCA o contrário** (camadas inferiores não conhecem superiores)
3. ✅ **Models Layer é usado por todas as camadas**
4. ✅ **Core Layer não depende de ninguém**

### Padrões Obrigatórios

#### 1. Dependency Injection (FastAPI)

```python
# ✅ Sempre usar Depends
@router.get("/items")
async def get_items(service: ItemService = Depends(get_item_service)):
    return await service.get_items()

# ❌ Nunca instanciar diretamente
@router.get("/items")
async def get_items():
    service = ItemService()  # ❌
    return await service.get_items()
```

#### 2. Async/Await para I/O

```python
# ✅ Async para I/O
async def get_items() -> List[ItemResponse]:
    async with ExternalAPIClient() as client:
        data = await client.get_data("/items")
    return data

# ❌ Sync para I/O
def get_items() -> List[ItemResponse]:
    client = ExternalAPIClient()
    data = client.get_data("/items")  # ❌
    return data
```

#### 3. Pydantic para Validação

```python
# ✅ Sempre usar Pydantic models
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

# ❌ Nunca usar dicts simples
def create_item(data: dict):  # ❌
    ...
```

#### 4. Settings via Pydantic

```python
# ✅ Usar Settings singleton
from app.core.config import settings

api_url = settings.api_base_url

# ❌ Nunca usar os.getenv diretamente
import os
api_url = os.getenv("API_BASE_URL")  # ❌
```

---

## 📚 Documentação

### Docstrings (Google Style)

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Descrição breve da função (uma linha).
    
    Descrição detalhada se necessário.
    
    Args:
        param1: Descrição do param1
        param2: Descrição do param2
    
    Returns:
        bool: Descrição do retorno
    
    Raises:
        ValueError: Quando param2 é negativo
    """
    ...
```

### Comentários

```python
# ✅ Explicar "por quê", não "o quê"
# Usamos lru_cache para garantir singleton (Settings carregado uma vez)
@lru_cache
def get_settings() -> Settings:
    return Settings()

# ❌ Comentários óbvios
# Cria uma lista
items = []  # ❌
```

### Documentação de Features

**Ao adicionar nova feature**:

1. Criar `.specs/features/[feature-name]/spec.md`
2. Documentar em `docs/api.md` (se for endpoint)
3. Atualizar `README.md` se necessário
4. Atualizar `.specs/project/ROADMAP.md`

---

## 🧪 Testes

### Cobertura Obrigatória

- **Meta geral**: >80%
- **Core modules**: >90%
- **Novos códigos**: 100%

### Estrutura de Testes

```
tests/
├── conftest.py          # Fixtures compartilhadas
├── test_auth.py         # Testa app/core/auth.py
├── test_client.py       # Testa app/clients/api_client.py
└── test_endpoints.py    # Testa app/api/routes/items.py
```

### Nomenclatura

```python
# ✅ Padrão: test_<função>_<cenário>_<resultado>
def test_get_items_returns_list(): ...
def test_create_item_with_valid_data_returns_created_item(): ...
def test_get_item_raises_404_when_not_found(): ...

# ❌ Evitar
def test1(): ...
def test_items(): ...
```

### AAA Pattern

```python
def test_create_item():
    # Arrange
    item_data = ItemCreate(name="Test", description="Test item")
    
    # Act
    result = service.create_item(item_data)
    
    # Assert
    assert result.name == "Test"
    assert result.id is not None
```

### Executar Testes

```bash
# SEMPRE rodar antes de commit
pytest
pytest -v  # Verbose
pytest --cov=app  # Com cobertura
```

---

## 🔄 Workflow de Desenvolvimento

### Antes de Modificar Código

1. ✅ Ler **AGENTS.md** (este arquivo)
2. ✅ Ler **.specs/project/STATE.md** (estado atual)
3. ✅ Ler **.specs/codebase/CONCERNS.md** (áreas frágeis)
4. ✅ Verificar se feature está no **ROADMAP.md**
5. ✅ Verificar **TODOs** em **STATE.md**

### Ao Adicionar Feature

1. ✅ Criar spec em `.specs/features/[feature]/spec.md`
2. ✅ Adicionar models em `app/models/schemas.py`
3. ✅ Criar service em `app/services/[feature]_service.py`
4. ✅ Criar endpoints em `app/api/routes/[feature].py`
5. ✅ Adicionar testes em `tests/test_[feature].py`
6. ✅ Atualizar documentação (`docs/`, `README.md`)
7. ✅ Atualizar **STATE.md** (decisões, TODOs)

### Ao Modificar Código Existente

1. ✅ Ler código existente e entender contexto
2. ✅ Verificar se há testes (rodar antes de modificar)
3. ✅ Fazer modificação
4. ✅ Atualizar/adicionar testes
5. ✅ Rodar `ruff format .` e `ruff check .`
6. ✅ Rodar `pytest` (todos os testes devem passar)
7. ✅ Atualizar documentação se necessário
8. ✅ Atualizar **STATE.md** se for decisão importante

### Ao Fazer Commit

```bash
# Formato: <tipo>: <descrição>
git commit -m "feat: adiciona endpoint de listagem de items"
git commit -m "fix: corrige validação de JWT expirado"
git commit -m "docs: atualiza README com instruções de instalação"
git commit -m "refactor: extrai lógica de autenticação para JWTManager"
```

**Tipos**:
- `feat`: Nova feature
- `fix`: Bug fix
- `docs`: Documentação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Manutenção

---

## ⚠️ Áreas Sensíveis

### 🔴 CRÍTICO: Não Modificar Sem Cuidado

#### 1. `app/core/auth.py` (JWT Manager)

**Fragilidade**: Alta

**Razões**:
- Token em memória (não persiste)
- Não suporta multi-instância
- Lógica de expiração crítica

**Cuidados**:
- ✅ Testar expiração de token
- ✅ Testar renovação automática
- ✅ Considerar race conditions
- ❌ NÃO quebrar cache de token
- ❌ NÃO mudar formato de token sem migração

---

#### 2. `app/clients/api_client.py` (HTTP Client)

**Fragilidade**: Média

**Razões**:
- Sem retry logic (tech debt)
- Injeção de JWT token crítica
- Error handling básico

**Cuidados**:
- ✅ Testar timeouts
- ✅ Testar error handling
- ❌ NÃO quebrar injeção de JWT
- ❌ NÃO remover async/await

---

#### 3. `app/core/config.py` (Settings)

**Fragilidade**: Média

**Razões**:
- Singleton pattern (lru_cache)
- Usado por toda aplicação
- Validação de .env

**Cuidados**:
- ✅ Manter singleton pattern
- ✅ Validar novos campos
- ❌ NÃO quebrar backward compatibility
- ❌ NÃO hardcodar valores

---

### 🟠 Atenção: Modificar com Testes

#### 4. `app/api/routes/items.py` (Endpoints)

**Cuidados**:
- ✅ Manter validação Pydantic
- ✅ Manter status codes corretos
- ✅ Atualizar testes de integração

---

#### 5. `app/models/schemas.py` (Pydantic Models)

**Cuidados**:
- ✅ Manter validação
- ✅ Backward compatibility
- ✅ Atualizar testes de validação

---

## ✅ Checklist de Modificações

### Antes de Commit

- [ ] Código segue PEP 8 (`ruff format .` executado)
- [ ] Type hints completos
- [ ] Docstrings em funções públicas
- [ ] Testes adicionados/atualizados
- [ ] Todos os testes passam (`pytest`)
- [ ] Sem secrets hardcoded
- [ ] Logging apropriado
- [ ] Error handling robusto
- [ ] Imports organizados
- [ ] Nomes descritivos
- [ ] Sem código comentado
- [ ] Documentação atualizada
- [ ] **STATE.md** atualizado (se decisão importante)

### Antes de PR

- [ ] Branch atualizada com main
- [ ] Todos os testes passam
- [ ] Cobertura de testes >80% (ou mantida)
- [ ] Documentação completa
- [ ] Commit messages descritivos
- [ ] Sem conflitos de merge
- [ ] **ROADMAP.md** atualizado (se nova feature)

---

## 🚫 Proibições Absolutas

### ❌ NUNCA Fazer

1. ❌ **Commitar arquivo `.env`** (secrets)
2. ❌ **Hardcodar secrets** (API keys, JWT_SECRET, etc.)
3. ❌ **Remover type hints** existentes
4. ❌ **Pular camadas** (ex: API → Client, sem Service)
5. ❌ **Usar `print()`** para logging (usar `logger`)
6. ❌ **Imports relativos** (`from ..core import ...`)
7. ❌ **Código sem testes** (cobertura deve aumentar ou manter)
8. ❌ **Modificar áreas críticas sem ler CONCERNS.md**
9. ❌ **Quebrar backward compatibility** sem migração
10. ❌ **Ignorar erros de `ruff` ou `pytest`**

---

## 📖 Referências Rápidas

### Documentos Essenciais

| Documento | Quando Ler |
|-----------|------------|
| **AGENTS.md** | Sempre, antes de qualquer modificação |
| **.specs/project/PROJECT.md** | Entender visão e objetivos |
| **.specs/project/STATE.md** | Ver estado atual, decisões, TODOs |
| **.specs/project/ROADMAP.md** | Planejar features |
| **.specs/codebase/ARCHITECTURE.md** | Entender arquitetura |
| **.specs/codebase/CONVENTIONS.md** | Seguir padrões de código |
| **.specs/codebase/CONCERNS.md** | Identificar áreas frágeis |
| **.specs/codebase/TESTING.md** | Estratégia de testes |
| **README.md** | Visão geral do projeto |
| **CONTRIBUTING.md** | Processo de contribuição |

### Comandos Essenciais

```bash
# Formatação e linting
ruff format .
ruff check .

# Testes
pytest
pytest -v
pytest --cov=app

# Rodar aplicação
python main.py
# ou
uvicorn main:app --reload
```

---

## 🎯 Objetivos de Qualidade

### Métricas Obrigatórias

- ✅ Cobertura de testes: >80%
- ✅ Type hints: 100%
- ✅ Ruff checks: 0 erros
- ✅ Documentação: Completa e atualizada
- ✅ Secrets: 0 hardcoded

### Princípios de Qualidade

1. **Código limpo**: Legível, manutenível, testável
2. **Documentação viva**: Sempre atualizada com código
3. **Testes confiáveis**: Rápidos, determinísticos, isolados
4. **Segurança first**: Sem secrets, validação robusta
5. **Performance consciente**: Async/await, connection pooling

---

## 📞 Dúvidas?

1. ✅ Ler documentação em `.specs/`
2. ✅ Verificar **STATE.md** (decisões passadas)
3. ✅ Verificar **CONCERNS.md** (tech debt)
4. ✅ Verificar **ROADMAP.md** (features planejadas)
5. ✅ Abrir issue no repositório

---

## 📝 Histórico de Atualizações

| Data | Versão | Mudanças |
|------|--------|----------|
| 2026-03-22 | 1.0.0 | Criação inicial do AGENTS.md |

---

**Lembre-se**: Este arquivo é a fonte única de verdade para padrões e regras do projeto. Em caso de conflito com outros documentos, **AGENTS.md tem prioridade**.
