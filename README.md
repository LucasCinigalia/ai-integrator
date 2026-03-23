# API Integrator

Aplicação Python profissional para consumir API REST externa com autenticação JWT, seguindo princípios de Clean Architecture.

## 📋 Descrição

API Integrator é uma aplicação base construída com FastAPI que demonstra boas práticas de engenharia de software, incluindo:

- **Clean Architecture**: Separação clara de responsabilidades em camadas
- **Autenticação JWT**: Gerenciamento automático de tokens
- **Async/Await**: Operações assíncronas para melhor performance
- **Type Safety**: Validação completa com Pydantic e type hints
- **Testes**: Cobertura de testes com pytest
- **Documentação**: Swagger UI e ReDoc automáticos

## 🏗️ Arquitetura

O projeto segue Clean Architecture com a seguinte estrutura de camadas:

```
┌─────────────────────────────────────┐
│      API Layer (FastAPI)            │  ← Endpoints REST
├─────────────────────────────────────┤
│      Services Layer                 │  ← Lógica de negócio
├─────────────────────────────────────┤
│      Clients Layer                  │  ← Integração com APIs externas
├─────────────────────────────────────┤
│      Models Layer (Pydantic)        │  ← Validação de dados
├─────────────────────────────────────┤
│      Core Layer                     │  ← Configurações, Auth, Constantes
└─────────────────────────────────────┘
```

### Estrutura de Diretórios

```
ai-integrator/
├── app/
│   ├── core/              # Configurações, constantes e autenticação
│   │   ├── config.py      # Settings com Pydantic
│   │   ├── constants.py   # Constantes da aplicação
│   │   └── auth.py        # Gerenciamento JWT
│   ├── models/            # Schemas Pydantic
│   │   └── schemas.py     # Modelos de dados
│   ├── clients/           # Clientes HTTP para APIs externas
│   │   └── api_client.py  # Cliente assíncrono com httpx
│   ├── services/          # Lógica de negócio
│   │   └── item_service.py
│   └── api/               # Endpoints FastAPI
│       ├── dependencies.py
│       └── routes/
│           └── items.py
├── tests/                 # Testes com pytest
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_client.py
│   └── test_endpoints.py
├── main.py               # Entry point da aplicação
├── requirements.txt      # Dependências
├── pyproject.toml       # Configuração do projeto
├── .env.example         # Template de variáveis de ambiente
└── README.md
```

## 🚀 Tecnologias

- **Python 3.10+**
- **FastAPI**: Framework web moderno e rápido
- **httpx**: Cliente HTTP assíncrono
- **Pydantic**: Validação de dados
- **python-jose**: Gerenciamento JWT
- **uvicorn**: Servidor ASGI
- **pytest**: Framework de testes

## 📦 Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone <repository-url>
cd ai-integrator
```

### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
# Linux/Mac
cp .env.example .env

# Windows (PowerShell)
copy .env.example .env

# Edite o arquivo .env com suas configurações
```

Variáveis disponíveis no `.env`:

```env
# API Configuration
API_BASE_URL=https://api.example.com
API_TIMEOUT=30

# JWT Configuration
JWT_SECRET=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
TOKEN_EXPIRY_MINUTES=30

# Application Configuration
APP_NAME=API Integrator
APP_VERSION=0.1.0
DEBUG=True

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## ▶️ Como Rodar

### Modo Desenvolvimento

```bash
# Opção 1: Usando uvicorn diretamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Opção 2: Executando o main.py
python main.py
```

A aplicação estará disponível em:
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Modo Produção

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🧪 Testes

### Executar todos os testes

```bash
pytest
```

### Executar com verbose

```bash
pytest -v
```

### Executar testes específicos

```bash
# Testes de autenticação
pytest tests/test_auth.py -v

# Testes de cliente HTTP
pytest tests/test_client.py -v

# Testes de endpoints
pytest tests/test_endpoints.py -v
```

### Cobertura de testes (opcional)

```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

## 📡 Endpoints disponíveis

### Health check

```http
GET /health
```

Retorna o status de saúde da aplicação.

### Items

#### Listar items

```http
GET /items
```

**Exemplo com curl:**
```bash
curl -X GET "http://localhost:8000/items"
```

#### Buscar item por ID

```http
GET /items/{item_id}
```

**Exemplo:**
```bash
curl -X GET "http://localhost:8000/items/550e8400-e29b-41d4-a716-446655440001"
```

#### Criar novo item

```http
POST /items
Content-Type: application/json

{
  "name": "Novo Item",
  "description": "Descrição do item"
}
```

**Exemplo:**
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "Notebook", "description": "Notebook Dell Inspiron"}'
```

#### Atualizar item

```http
PUT /items/{item_id}
Content-Type: application/json

{
  "name": "Item Atualizado",
  "description": "Nova descrição"
}
```

**Exemplo:**
```bash
curl -X PUT "http://localhost:8000/items/550e8400-e29b-41d4-a716-446655440001" \
  -H "Content-Type: application/json" \
  -d '{"name": "Notebook Atualizado"}'
```

#### Deletar item

```http
DELETE /items/{item_id}
```

**Exemplo:**
```bash
curl -X DELETE "http://localhost:8000/items/550e8400-e29b-41d4-a716-446655440001"
```

### RD Station Conversas

#### Histórico de mensagens

```http
GET /api/v1/rd-conversas/messages/history
```

**Parâmetros de query:**
- `limit` (opcional): Número de mensagens (1-100, padrão: 50)
- `offset` (opcional): Offset para paginação (padrão: 0)
- `contact_phone` (opcional): Filtrar por telefone
- `start_date` (opcional): Data inicial (ISO 8601)
- `end_date` (opcional): Data final (ISO 8601)

**Exemplo:**
```bash
curl -X GET "http://localhost:8000/api/v1/rd-conversas/messages/history?limit=50&offset=0"
```

**Configuração necessária (.env):**
- `API_BASE_URL`: URL da API Tallos (`https://api.tallos.com.br/v2`)
- `API_TOKEN`: Bearer Token válido do RD Station Conversas
- `RD_CONVERSAS_PRIVATE_KEY_PATH` (opcional): Caminho para chave JWK para descriptografia

## 🔐 Autenticação

O sistema implementa gerenciamento automático de tokens JWT através da classe `JWTManager`:

- Tokens são gerados automaticamente quando necessário
- Tokens expirados são renovados automaticamente
- Tokens são injetados automaticamente nos headers das requisições HTTP

### Como funciona

1. O `JWTManager` mantém um token em cache
2. Antes de cada requisição, verifica se o token ainda é válido
3. Se expirado, gera um novo token automaticamente
4. O `ExternalAPIClient` injeta o token no header `Authorization`

## 🎯 Próximos Passos

### Integração com API Real

Atualmente o projeto usa dados mockados. Para integrar com uma API real:

1. Configure a `API_BASE_URL` no `.env`
2. Atualize o `ItemService` para usar o `ExternalAPIClient`:

```python
from app.clients.api_client import ExternalAPIClient

class ItemService:
    async def get_items(self) -> List[ItemResponse]:
        async with ExternalAPIClient() as client:
            data = await client.get_data("/items")
            return [ItemResponse(**item) for item in data]
```

### Melhorias Sugeridas

- [ ] Adicionar rate limiting
- [ ] Implementar cache com Redis
- [ ] Adicionar logging estruturado
- [ ] Implementar retry logic com backoff exponencial
- [ ] Adicionar métricas e observabilidade
- [ ] Implementar paginação nos endpoints
- [ ] Adicionar filtros e ordenação
- [ ] Criar Dockerfile para containerização
- [ ] Adicionar CI/CD pipeline
- [ ] Implementar autenticação de usuários

## 🤝 Decisões Arquiteturais

### 1. Clean Architecture
Separação clara entre camadas facilita manutenção e testes. Cada camada tem responsabilidade única e bem definida.

### 2. Dependency injection
O `Depends` do FastAPI permite injeção de dependências, facilitando testes e substituição de implementações.

### 3. Async first
Todas as operações I/O são assíncronas (httpx, FastAPI) para melhor performance e escalabilidade.

### 4. Type safety
Type hints completos e Pydantic garantem validação em tempo de execução e melhor suporte a IDE.

### 5. Configuração externa
Todas as configurações via `.env`, sem hardcoding, seguindo princípios 12-factor app.

### 6. Testabilidade
Serviços mockados e injeção de dependência facilitam testes unitários e de integração.

## 📝 Licença

Este projeto é um template de código aberto para fins educacionais e pode ser usado livremente.

## 👥 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

**Para contribuir com código:**
1. Leia o [AGENTS.md](AGENTS.md) - Regras e padrões do projeto
2. Consulte [.specs/](.specs/) - Especificações e documentação técnica
3. Siga o [guia de contribuição](CONTRIBUTING.md)

**Para contribuir com documentação:**
1. Siga o [padrão de documentação](DOCS_STANDARD.md)
2. Consulte o [guia de estilo](references/style-guide.md)

## 📚 Documentação Adicional

Este projeto segue o padrão **tlc-spec-driven** para documentação estruturada:

- **[AGENTS.md](AGENTS.md)** - 🔴 Regras e padrões para agentes de IA e desenvolvedores
- **[.specs/](.specs/)** - Especificações completas do projeto
  - `project/` - Visão, roadmap, estado atual
  - `codebase/` - Análise técnica (arquitetura, stack, convenções)
  - `features/` - Especificações de features
  - `quick/` - Tasks rápidas
- **[docs/](docs/)** - Documentação técnica detalhada
- **[references/](references/)** - Guias de referência

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.
