# Stack Tecnológica - API Integrator

## Linguagem e Runtime

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **Python** | 3.10+ | Linguagem principal |
| **pip** | Latest | Gerenciador de pacotes |
| **venv** | Built-in | Ambiente virtual |

## Framework Web

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **FastAPI** | 0.110+ | Framework web assíncrono, geração automática de docs |
| **uvicorn** | 0.27+ | Servidor ASGI para FastAPI |
| **Starlette** | - | Base do FastAPI (dependência transitiva) |

## Cliente HTTP

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **httpx** | 0.27+ | Cliente HTTP assíncrono para consumir APIs externas |

## Validação e Schemas

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **Pydantic** | 2.6+ | Validação de dados, schemas, serialização |
| **pydantic-settings** | 2.2+ | Gerenciamento de configurações via .env |

## Autenticação e Segurança

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **python-jose** | 3.3+ | Criação e validação de tokens JWT |
| **cryptography** | - | Criptografia (dependência do python-jose) |

## Configuração

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **python-dotenv** | 1.0+ | Carregamento de variáveis de ambiente do .env |

## Testes

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **pytest** | 8.1+ | Framework de testes |
| **pytest-asyncio** | 0.23+ | Suporte a testes assíncronos |

## Linting e Formatação

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **ruff** | - | Linter e formatter (configurado no pyproject.toml) |

## Dependências Futuras (Roadmap)

| Tecnologia | Milestone | Propósito |
|------------|-----------|-----------|
| **Redis** | v0.3.0 | Cache de respostas |
| **Prometheus Client** | v0.4.0 | Métricas |
| **OpenTelemetry** | v0.4.0 | Distributed tracing |
| **Docker** | v0.5.0 | Containerização |

## Arquitetura de Dependências

```
FastAPI (web framework)
├── Starlette (ASGI framework)
├── Pydantic (validation)
└── uvicorn (ASGI server)

httpx (HTTP client)
└── httpcore (low-level HTTP)

python-jose (JWT)
└── cryptography (crypto operations)

pydantic-settings (config)
├── Pydantic
└── python-dotenv

pytest (testing)
└── pytest-asyncio (async support)
```

## Decisões de Stack

### Por que FastAPI?

- ✅ Performance (um dos frameworks Python mais rápidos)
- ✅ Async/await nativo
- ✅ Documentação automática (Swagger/ReDoc)
- ✅ Validação automática com Pydantic
- ✅ Type hints completos
- ✅ Comunidade ativa e crescente

### Por que httpx em vez de requests?

- ✅ Suporte a async/await
- ✅ HTTP/2 support
- ✅ Connection pooling
- ✅ API similar ao requests (fácil migração)
- ✅ Mantido ativamente

### Por que Pydantic v2?

- ✅ Performance (core em Rust)
- ✅ Validação robusta
- ✅ Integração nativa com FastAPI
- ✅ Type safety completo
- ✅ JSON Schema generation

### Por que python-jose para JWT?

- ✅ Suporte a múltiplos algoritmos
- ✅ Bem testado e maduro
- ✅ Recomendado pela documentação do FastAPI
- ✅ Fácil de usar

### Por que pytest?

- ✅ Padrão de facto para testes em Python
- ✅ Fixtures poderosas
- ✅ Plugins extensivos (pytest-asyncio, pytest-cov, etc.)
- ✅ Sintaxe simples e clara

## Versões Mínimas

Definidas em `pyproject.toml`:

```toml
requires-python = ">=3.10"
```

Python 3.10 foi escolhido por:
- ✅ Pattern matching (structural pattern matching)
- ✅ Better error messages
- ✅ Type hints improvements
- ✅ Performance improvements
- ✅ Ainda amplamente suportado (não cutting edge)

## Compatibilidade

| Ambiente | Suportado | Notas |
|----------|-----------|-------|
| **Windows** | ✅ | Testado no Windows 10+ |
| **Linux** | ✅ | Testado no Ubuntu 20.04+ |
| **macOS** | ✅ | Testado no macOS 12+ |
| **Docker** | 🔜 | Planejado para v0.5.0 |

## Instalação

### Desenvolvimento

```bash
pip install -r requirements.txt
```

### Produção (futuro)

```bash
pip install -r requirements.txt --no-dev
```

## Atualizações de Dependências

Para atualizar dependências:

```bash
# Verificar versões desatualizadas
pip list --outdated

# Atualizar requirements.txt
pip install --upgrade <package>
pip freeze > requirements.txt
```

**Importante**: Sempre testar após atualizar dependências.
