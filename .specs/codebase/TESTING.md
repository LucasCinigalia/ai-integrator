# Estratégia de Testes - API Integrator

## Visão Geral

Estratégia de testes abrangente cobrindo diferentes níveis de teste, desde unitários até integração.

**Framework**: pytest  
**Cobertura atual**: ~70%  
**Meta**: >80%

---

## Pirâmide de Testes

```
        ┌─────────────┐
        │   E2E       │  ← Poucos (futuro)
        └─────────────┘
      ┌─────────────────┐
      │  Integration    │  ← Alguns
      └─────────────────┘
    ┌─────────────────────┐
    │      Unit           │  ← Muitos
    └─────────────────────┘
```

### Unit Tests (Muitos)

**Foco**: Testar unidades isoladas (funções, classes, métodos).

**Características**:
- Rápidos (<10ms cada)
- Sem dependências externas (mocks)
- Alta cobertura de código

**Exemplos**:
- Validação de Pydantic models
- Lógica de negócio em services
- Funções utilitárias
- JWT generation/validation

---

### Integration Tests (Alguns)

**Foco**: Testar integração entre componentes.

**Características**:
- Mais lentos (100-500ms cada)
- Podem usar dependências reais (API externa mockada)
- Testam fluxo completo

**Exemplos**:
- Endpoints FastAPI (request → response)
- Service + Client integration
- Database operations (futuro)

---

### E2E Tests (Poucos) - Futuro

**Foco**: Testar aplicação completa em ambiente real.

**Características**:
- Lentos (>1s cada)
- Ambiente real ou staging
- Testam casos de uso críticos

**Exemplos**:
- Fluxo completo de criação de item
- Autenticação end-to-end
- Error handling em produção

---

## Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartilhadas
├── test_auth.py             # Unit: JWT Manager
├── test_client.py           # Unit + Integration: HTTP Client
└── test_endpoints.py        # Integration: FastAPI endpoints
```

---

## Arquivos de Teste

### `conftest.py` - Fixtures Compartilhadas

**Propósito**: Definir fixtures reutilizáveis.

**Fixtures principais**:
```python
@pytest.fixture
def settings():
    """Fixture para Settings de teste."""
    return Settings(
        api_base_url="https://test-api.example.com",
        jwt_secret="test-secret",
        debug=True
    )

@pytest.fixture
def jwt_manager(settings):
    """Fixture para JWTManager."""
    return JWTManager(settings)

@pytest.fixture
async def client():
    """Fixture para TestClient do FastAPI."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
```

---

### `test_auth.py` - Testes de Autenticação

**Foco**: JWT Manager (geração, validação, expiração).

**Testes**:
```python
def test_generate_token_creates_valid_jwt(jwt_manager):
    """Testa geração de token JWT válido."""
    token = jwt_manager.generate_token()
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

def test_is_token_valid_returns_true_for_valid_token(jwt_manager):
    """Testa validação de token válido."""
    token = jwt_manager.generate_token()
    assert jwt_manager.is_token_valid(token) is True

def test_is_token_valid_returns_false_for_expired_token(jwt_manager):
    """Testa validação de token expirado."""
    # Cria token com expiração no passado
    expired_token = jwt_manager.generate_token(expiry_minutes=-1)
    assert jwt_manager.is_token_valid(expired_token) is False

def test_get_token_returns_cached_token_when_valid(jwt_manager):
    """Testa cache de token válido."""
    token1 = jwt_manager.get_token()
    token2 = jwt_manager.get_token()
    assert token1 == token2  # Mesmo token (cache)

def test_get_token_generates_new_token_when_expired(jwt_manager):
    """Testa renovação de token expirado."""
    # Força expiração
    jwt_manager._token = "expired_token"
    new_token = jwt_manager.get_token()
    assert new_token != "expired_token"
```

**Cobertura**: ~90%

---

### `test_client.py` - Testes de Cliente HTTP

**Foco**: ExternalAPIClient (requisições, error handling).

**Testes**:
```python
@pytest.mark.asyncio
async def test_client_injects_jwt_token(respx_mock):
    """Testa injeção automática de JWT token."""
    respx_mock.get("https://api.example.com/items").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    
    async with ExternalAPIClient() as client:
        await client.get_data("/items")
    
    # Verifica que Authorization header foi enviado
    request = respx_mock.calls.last.request
    assert "Authorization" in request.headers
    assert request.headers["Authorization"].startswith("Bearer ")

@pytest.mark.asyncio
async def test_client_handles_timeout(respx_mock):
    """Testa tratamento de timeout."""
    respx_mock.get("https://api.example.com/items").mock(
        side_effect=httpx.TimeoutException
    )
    
    async with ExternalAPIClient() as client:
        with pytest.raises(httpx.TimeoutException):
            await client.get_data("/items")

@pytest.mark.asyncio
async def test_client_handles_http_error(respx_mock):
    """Testa tratamento de erro HTTP."""
    respx_mock.get("https://api.example.com/items").mock(
        return_value=httpx.Response(500, json={"error": "Internal error"})
    )
    
    async with ExternalAPIClient() as client:
        with pytest.raises(httpx.HTTPStatusError):
            response = await client.get_data("/items")
            response.raise_for_status()
```

**Ferramentas**:
- `respx`: Mock de requisições httpx
- `pytest-asyncio`: Suporte a testes assíncronos

**Cobertura**: ~80%

---

### `test_endpoints.py` - Testes de Endpoints

**Foco**: Endpoints FastAPI (integration tests).

**Testes**:
```python
@pytest.mark.asyncio
async def test_get_items_returns_list(client):
    """Testa GET /items retorna lista."""
    response = await client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_item_by_id_returns_item(client):
    """Testa GET /items/{id} retorna item."""
    item_id = "550e8400-e29b-41d4-a716-446655440001"
    response = await client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id

@pytest.mark.asyncio
async def test_get_item_by_id_returns_404_when_not_found(client):
    """Testa GET /items/{id} retorna 404 quando não encontrado."""
    item_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/items/{item_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_item_returns_created_item(client):
    """Testa POST /items cria item."""
    item_data = {
        "name": "Test Item",
        "description": "Test description"
    }
    response = await client.post("/items", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_item_validates_input(client):
    """Testa validação de input em POST /items."""
    invalid_data = {"name": ""}  # Nome vazio (inválido)
    response = await client.post("/items", json=invalid_data)
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_update_item_returns_updated_item(client):
    """Testa PUT /items/{id} atualiza item."""
    item_id = "550e8400-e29b-41d4-a716-446655440001"
    update_data = {"name": "Updated Name"}
    response = await client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

@pytest.mark.asyncio
async def test_delete_item_returns_success(client):
    """Testa DELETE /items/{id} deleta item."""
    item_id = "550e8400-e29b-41d4-a716-446655440001"
    response = await client.delete(f"/items/{item_id}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_health_check_returns_healthy(client):
    """Testa GET /health retorna status healthy."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
```

**Ferramentas**:
- `httpx.AsyncClient`: Cliente HTTP para testes
- `TestClient` do FastAPI (alternativa)

**Cobertura**: ~70%

---

## Padrões de Teste

### AAA Pattern (Arrange-Act-Assert)

```python
def test_example():
    # Arrange: Preparar dados e mocks
    item_data = ItemCreate(name="Test", description="Test item")
    
    # Act: Executar ação
    result = service.create_item(item_data)
    
    # Assert: Verificar resultado
    assert result.name == "Test"
    assert result.id is not None
```

---

### Nomenclatura de Testes

**Padrão**: `test_<função>_<cenário>_<resultado_esperado>`

**Exemplos**:
```python
# ✅ Bom
def test_get_items_returns_list(): ...
def test_create_item_with_valid_data_returns_created_item(): ...
def test_get_item_raises_404_when_not_found(): ...

# ❌ Evitar
def test1(): ...
def test_items(): ...
def test_error(): ...
```

---

### Fixtures vs Setup/Teardown

**Preferir fixtures** (mais flexível):
```python
@pytest.fixture
def item_service():
    return ItemService()

def test_get_items(item_service):
    result = item_service.get_items()
    assert len(result) > 0
```

**Evitar setup/teardown** (menos flexível):
```python
class TestItemService:
    def setup_method(self):
        self.service = ItemService()
    
    def test_get_items(self):
        result = self.service.get_items()
        assert len(result) > 0
```

---

### Mocking

**Ferramentas**:
- `unittest.mock`: Mock de objetos Python
- `respx`: Mock de requisições httpx
- `pytest-mock`: Plugin pytest para mocking

**Exemplo**:
```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_service_calls_client():
    """Testa que service chama client."""
    mock_client = AsyncMock()
    mock_client.get_data.return_value = [{"id": "1", "name": "Test"}]
    
    service = ItemService(client=mock_client)
    result = await service.get_items()
    
    mock_client.get_data.assert_called_once_with("/items")
    assert len(result) == 1
```

---

## Executando Testes

### Todos os Testes

```bash
pytest
```

### Testes Específicos

```bash
# Por arquivo
pytest tests/test_auth.py

# Por função
pytest tests/test_auth.py::test_generate_token_creates_valid_jwt

# Por padrão
pytest -k "test_get"
```

### Com Verbose

```bash
pytest -v
```

### Com Cobertura

```bash
pytest --cov=app
pytest --cov=app --cov-report=html
```

### Apenas Testes Rápidos

```bash
pytest -m "not slow"
```

---

## Configuração do pytest

**`pyproject.toml`**:
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests"
]
```

---

## Cobertura de Testes

### Atual

| Módulo | Cobertura |
|--------|-----------|
| `app/core/auth.py` | ~90% |
| `app/core/config.py` | ~80% |
| `app/clients/api_client.py` | ~80% |
| `app/services/item_service.py` | ~60% |
| `app/api/routes/items.py` | ~70% |
| `app/models/schemas.py` | ~50% |
| **Total** | **~70%** |

### Meta

- **Geral**: >80%
- **Core modules**: >90%
- **API endpoints**: >80%
- **Services**: >80%

---

## Gaps de Teste (TODOs)

### Prioridade Alta

- [ ] Adicionar testes para error handling em endpoints
- [ ] Adicionar testes para validação de Pydantic models
- [ ] Adicionar testes para edge cases (valores extremos)

### Prioridade Média

- [ ] Adicionar testes de performance (load testing)
- [ ] Adicionar testes de segurança (SQL injection, XSS)
- [ ] Adicionar testes de concorrência

### Prioridade Baixa

- [ ] Adicionar E2E tests (Playwright/Selenium)
- [ ] Adicionar mutation testing
- [ ] Adicionar property-based testing (Hypothesis)

---

## CI/CD (Futuro)

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v3
```

---

## Boas Práticas

### ✅ Fazer

- Testar comportamento, não implementação
- Um assert por teste (quando possível)
- Testes independentes (não dependem de ordem)
- Nomes descritivos
- Usar fixtures para setup
- Mockar dependências externas
- Testar edge cases

### ❌ Evitar

- Testes que dependem de ordem de execução
- Testes que dependem de estado global
- Testes que chamam APIs reais
- Testes lentos sem necessidade
- Múltiplos conceitos em um teste
- Testes sem asserts
- Código duplicado entre testes

---

## Ferramentas Adicionais (Futuro)

| Ferramenta | Propósito |
|------------|-----------|
| **pytest-cov** | Cobertura de testes |
| **pytest-xdist** | Paralelização de testes |
| **pytest-benchmark** | Performance testing |
| **Hypothesis** | Property-based testing |
| **Locust** | Load testing |
| **Bandit** | Security testing |

---

## Referências

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [respx Documentation](https://lundberg.github.io/respx/)
- [Testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
