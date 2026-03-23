# Arquitetura

O API Integrator segue Clean Architecture com camadas bem definidas.

## Camadas

| Camada | Diretório | Responsabilidade |
|--------|-----------|------------------|
| API | `app/api/` | Endpoints REST, dependências FastAPI |
| Services | `app/services/` | Lógica de negócio |
| Clients | `app/clients/` | Integração com APIs externas |
| Models | `app/models/` | Schemas Pydantic |
| Core | `app/core/` | Configuração, autenticação JWT, constantes |

## Fluxo de dados

Requisição HTTP → API Layer → Services → Clients → API externa → Resposta

## Decisões principais

- **Async first:** Operações I/O assíncronas com httpx e FastAPI
- **Dependency injection:** FastAPI `Depends` para testabilidade
- **Configuração externa:** Variáveis via `.env`, sem hardcoding
- **Type safety:** Pydantic e type hints em todo o fluxo
