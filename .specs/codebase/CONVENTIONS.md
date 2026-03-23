# Convenções de Código - API Integrator

Este documento define as convenções de código, estilo e boas práticas do projeto.

## Linguagem e Estilo

### Idioma

- **Código**: Inglês (nomes de variáveis, funções, classes, comentários inline)
- **Documentação**: Português (README, docs/, .specs/)
- **Commits**: Português
- **Docstrings**: Português

**Exemplo**:
```python
def get_items() -> List[ItemResponse]:
    """
    Retorna lista de items.
    
    Returns:
        List[ItemResponse]: Lista de items
    """
    items = []  # Código em inglês
    return items
```

---

## Python Style Guide

### Base: PEP 8

Seguimos [PEP 8](https://peps.python.org/pep-0008/) com algumas customizações.

### Formatação

**Ferramenta**: `ruff` (configurado em `pyproject.toml`)

```bash
# Formatar código
ruff format .

# Verificar linting
ruff check .
```

**Configuração** (`pyproject.toml`):
```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
```

### Line Length

- **Máximo**: 100 caracteres
- **Preferível**: 80-90 caracteres
- **Strings longas**: Quebrar em múltiplas linhas

**Exemplo**:
```python
# ✅ Bom
error_message = (
    "Erro ao processar requisição: "
    f"status={status_code}, details={details}"
)

# ❌ Evitar
error_message = f"Erro ao processar requisição: status={status_code}, details={details}, timestamp={timestamp}, user={user_id}"
```

---

## Nomenclatura

### Variáveis e Funções

- **snake_case**: Variáveis, funções, métodos
- **Descritivo**: Nome deve indicar propósito
- **Evitar abreviações**: Exceto convenções conhecidas (id, url, http, jwt)

```python
# ✅ Bom
user_id: UUID
api_base_url: str
def get_items() -> List[ItemResponse]: ...

# ❌ Evitar
uid: UUID
url: str  # Muito genérico
def get() -> List: ...  # Não descritivo
```

### Classes

- **PascalCase**: Classes, Exceptions
- **Substantivos**: Classes representam entidades
- **Sufixos comuns**: Service, Client, Manager, Response, Request

```python
# ✅ Bom
class ItemService: ...
class ExternalAPIClient: ...
class JWTManager: ...
class ItemResponse(BaseModel): ...

# ❌ Evitar
class item_service: ...  # snake_case
class GetItems: ...  # Verbo
```

### Constantes

- **UPPER_SNAKE_CASE**: Constantes
- **Definir em**: `app/core/constants.py`

```python
# ✅ Bom
API_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PAGE_SIZE = 20

# ❌ Evitar
ApiTimeout = 30  # PascalCase
max_retries = 3  # snake_case (variável)
```

### Arquivos e Módulos

- **snake_case**: Nomes de arquivos
- **Descritivo**: Nome indica conteúdo
- **Singular**: Exceto quando plural faz sentido (routes, models)

```
# ✅ Bom
item_service.py
api_client.py
schemas.py

# ❌ Evitar
ItemService.py  # PascalCase
client.py  # Muito genérico
```

---

## Type Hints

### Obrigatório

- ✅ **Todos** os parâmetros de função
- ✅ **Todos** os retornos de função
- ✅ **Todos** os atributos de classe
- ✅ Variáveis quando tipo não é óbvio

### Imports

```python
from typing import List, Dict, Optional, Union, Any
from uuid import UUID
from datetime import datetime
```

### Exemplos

```python
# ✅ Bom - Type hints completos
def get_item(item_id: UUID) -> Optional[ItemResponse]:
    """Busca item por ID."""
    ...

async def create_item(data: ItemCreate) -> ItemResponse:
    """Cria novo item."""
    ...

class ItemService:
    def __init__(self, client: ExternalAPIClient) -> None:
        self.client: ExternalAPIClient = client

# ❌ Evitar - Sem type hints
def get_item(item_id):
    ...

def create_item(data):
    ...
```

### Optional vs Union

```python
# ✅ Preferir Optional
def get_item(item_id: UUID) -> Optional[ItemResponse]: ...

# ❌ Evitar Union com None
def get_item(item_id: UUID) -> Union[ItemResponse, None]: ...
```

---

## Docstrings

### Formato: Google Style

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Descrição breve da função (uma linha).
    
    Descrição detalhada se necessário (parágrafo).
    Pode ter múltiplas linhas.
    
    Args:
        param1: Descrição do param1
        param2: Descrição do param2
    
    Returns:
        bool: Descrição do retorno
    
    Raises:
        ValueError: Quando param2 é negativo
        HTTPException: Quando API externa falha
    
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    ...
```

### Classes

```python
class ItemService:
    """
    Serviço para gerenciamento de items.
    
    Responsável por orquestrar operações de CRUD de items,
    incluindo validação e transformação de dados.
    
    Attributes:
        client: Cliente HTTP para API externa
    """
    
    def __init__(self, client: ExternalAPIClient) -> None:
        """
        Inicializa o serviço.
        
        Args:
            client: Cliente HTTP configurado
        """
        self.client = client
```

### Módulos

```python
"""
Serviços de negócio da aplicação.

Este módulo contém a lógica de negócio e orquestração
de operações entre diferentes camadas.
"""
```

---

## Imports

### Ordem

1. Standard library
2. Third-party packages
3. Local application imports

**Separar com linha em branco entre grupos.**

```python
# ✅ Bom
import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.config import settings
from app.models.schemas import ItemResponse
from app.services.item_service import ItemService

# ❌ Evitar - Sem organização
from app.models.schemas import ItemResponse
import logging
from fastapi import APIRouter
from uuid import UUID
```

### Imports Absolutos

```python
# ✅ Bom - Imports absolutos
from app.core.config import settings
from app.models.schemas import ItemResponse

# ❌ Evitar - Imports relativos
from ..core.config import settings
from ..models.schemas import ItemResponse
```

### Import Específico vs Import *

```python
# ✅ Bom - Import específico
from typing import List, Optional, Dict

# ❌ Evitar - Import *
from typing import *
```

---

## Async/Await

### Quando usar async

- ✅ Operações I/O (HTTP, DB, file)
- ✅ Endpoints FastAPI
- ✅ Funções que chamam outras async functions

### Quando NÃO usar async

- ❌ Operações CPU-bound
- ❌ Funções puramente computacionais
- ❌ Quando não há I/O

### Padrões

```python
# ✅ Bom - Async para I/O
async def get_items() -> List[ItemResponse]:
    async with ExternalAPIClient() as client:
        data = await client.get_data("/items")
    return data

# ✅ Bom - Sync para computação
def calculate_total(items: List[Item]) -> float:
    return sum(item.price for item in items)

# ❌ Evitar - Async sem I/O
async def calculate_total(items: List[Item]) -> float:
    return sum(item.price for item in items)
```

---

## Error Handling

### Exceptions

```python
# ✅ Bom - Específico
try:
    result = await client.get_data("/items")
except httpx.HTTPStatusError as e:
    logger.error(f"API error: {e.response.status_code}")
    raise HTTPException(status_code=502, detail="External API error")
except httpx.TimeoutException:
    logger.error("API timeout")
    raise HTTPException(status_code=504, detail="External API timeout")

# ❌ Evitar - Genérico
try:
    result = await client.get_data("/items")
except Exception as e:
    raise HTTPException(status_code=500, detail="Error")
```

### FastAPI HTTPException

```python
# ✅ Bom
from fastapi import HTTPException, status

raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not found"
)

# ❌ Evitar - Magic numbers
raise HTTPException(status_code=404, detail="Not found")
```

---

## Logging

### Níveis

- **DEBUG**: Informações detalhadas para debugging
- **INFO**: Eventos importantes (startup, requests)
- **WARNING**: Situações inesperadas mas recuperáveis
- **ERROR**: Erros que impedem operação específica
- **CRITICAL**: Erros que impedem funcionamento da aplicação

### Padrões

```python
import logging

logger = logging.getLogger(__name__)

# ✅ Bom
logger.info(f"Processing request for item_id={item_id}")
logger.error(f"Failed to fetch item: {str(e)}", exc_info=True)

# ❌ Evitar
print(f"Processing item {item_id}")  # Usar logger, não print
logger.error("Error")  # Sem contexto
```

---

## Pydantic Models

### Convenções

```python
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class ItemBase(BaseModel):
    """Schema base para Item."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ItemCreate(ItemBase):
    """Schema para criar Item."""
    pass

class ItemResponse(ItemBase):
    """Schema de resposta para Item."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Pydantic v2
```

### Field Validation

```python
# ✅ Bom - Validação explícita
name: str = Field(..., min_length=1, max_length=100, description="Nome do item")
price: float = Field(..., gt=0, description="Preço deve ser positivo")

# ❌ Evitar - Sem validação
name: str
price: float
```

---

## Testes

### Nomenclatura

```python
# ✅ Bom
def test_get_items_returns_list(): ...
def test_create_item_with_valid_data(): ...
def test_get_item_raises_404_when_not_found(): ...

# ❌ Evitar
def test1(): ...
def test_items(): ...  # Não descritivo
```

### Estrutura (AAA Pattern)

```python
def test_create_item_with_valid_data():
    # Arrange
    item_data = ItemCreate(name="Test", description="Test item")
    
    # Act
    result = await service.create_item(item_data)
    
    # Assert
    assert result.name == "Test"
    assert result.id is not None
```

### Fixtures

```python
# conftest.py
import pytest

@pytest.fixture
def item_service():
    """Fixture para ItemService."""
    return ItemService()

@pytest.fixture
def sample_item():
    """Fixture para item de teste."""
    return ItemCreate(name="Test", description="Test item")
```

---

## Configuração

### Variáveis de Ambiente

```python
# ✅ Bom - Usar Pydantic Settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_base_url: str = Field(default="https://api.example.com")
    api_timeout: int = Field(default=30)
    
    class Config:
        env_file = ".env"

# ❌ Evitar - os.getenv direto
import os
api_url = os.getenv("API_BASE_URL", "https://api.example.com")
```

---

## Comentários

### Quando comentar

- ✅ **Por quê**, não **o quê**
- ✅ Decisões não óbvias
- ✅ Workarounds temporários (com TODO)
- ✅ Algoritmos complexos

### Quando NÃO comentar

- ❌ Código auto-explicativo
- ❌ Comentários óbvios
- ❌ Código comentado (deletar)

```python
# ✅ Bom
# Usamos lru_cache para garantir singleton (Settings carregado uma vez)
@lru_cache
def get_settings() -> Settings:
    return Settings()

# TODO: Implementar retry logic quando API externa estiver instável
async def get_data(url: str) -> dict:
    ...

# ❌ Evitar
# Cria uma lista
items = []

# Loop pelos items
for item in items:
    # Imprime o item
    print(item)
```

---

## Git Commits

### Formato

```
<tipo>: <descrição curta>

<descrição detalhada opcional>
```

### Tipos

- **feat**: Nova feature
- **fix**: Bug fix
- **docs**: Documentação
- **refactor**: Refatoração (sem mudança de comportamento)
- **test**: Adicionar/modificar testes
- **chore**: Tarefas de manutenção

### Exemplos

```bash
# ✅ Bom
feat: adiciona endpoint de listagem de items
fix: corrige validação de JWT expirado
docs: atualiza README com instruções de instalação
refactor: extrai lógica de autenticação para JWTManager

# ❌ Evitar
update
fix bug
changes
WIP
```

---

## Checklist de Code Review

- [ ] Code segue PEP 8 (ruff format)
- [ ] Type hints completos
- [ ] Docstrings em funções públicas
- [ ] Testes adicionados/atualizados
- [ ] Sem secrets hardcoded
- [ ] Logging apropriado
- [ ] Error handling robusto
- [ ] Imports organizados
- [ ] Nomes descritivos
- [ ] Sem código comentado

---

## Ferramentas

### Obrigatórias

```bash
# Formatação e linting
ruff format .
ruff check .

# Testes
pytest
pytest -v  # Verbose
pytest --cov=app  # Com cobertura
```

### Recomendadas

```bash
# Type checking (futuro)
mypy app/

# Security scanning (futuro)
bandit -r app/
```

---

## Referências

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
