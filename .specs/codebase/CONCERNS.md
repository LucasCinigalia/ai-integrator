# Concerns, Tech Debt e Riscos - API Integrator

Este documento identifica áreas de preocupação, dívida técnica e riscos do projeto.

**Última atualização**: 2026-03-22

---

## 🔴 Crítico

### 1. JWT Token em Memória (Não Persiste)

**Descrição**: Token JWT é cacheado em memória no `JWTManager`. Se a aplicação reiniciar, o token é perdido.

**Impacto**: 
- ❌ Novo token gerado a cada restart
- ❌ Não funciona em ambiente multi-instância (load balancer)
- ❌ Não há compartilhamento de token entre workers

**Localização**: `app/core/auth.py` (linha ~30)

**Solução proposta**:
```python
# Opção 1: Redis cache (v0.3.0)
class JWTManager:
    async def get_token(self) -> str:
        cached = await redis.get("jwt:token")
        if cached and self.is_token_valid(cached):
            return cached
        
        token = self.generate_token()
        await redis.setex("jwt:token", self.expiry_seconds, token)
        return token

# Opção 2: Shared memory (multiprocessing)
# Opção 3: Database (overkill para token)
```

**Prioridade**: Alta (v0.3.0)  
**Workaround**: Aceitável para single-instance deployment

---

### 2. Sem Retry Logic

**Descrição**: Requisições HTTP não têm retry automático em caso de falhas transientes.

**Impacto**:
- ❌ Falhas temporárias causam erro imediato
- ❌ Não resiliente a instabilidades de rede
- ❌ Experiência ruim para usuário

**Localização**: `app/clients/api_client.py`

**Solução proposta**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

class ExternalAPIClient:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_data(self, endpoint: str) -> dict:
        ...
```

**Prioridade**: Alta (v0.2.0)  
**Workaround**: Manual retry no service layer

---

### 3. Secrets Hardcoded em .env (Versionado)

**Descrição**: Arquivo `.env` pode ser acidentalmente commitado com secrets reais.

**Impacto**:
- 🔥 **CRÍTICO**: Exposição de secrets (JWT_SECRET, API keys)
- 🔥 Comprometimento de segurança

**Localização**: `.env`

**Solução proposta**:
1. ✅ `.env` já está no `.gitignore`
2. 🔜 Adicionar pre-commit hook para validar (v0.6.0)
3. 🔜 Usar secrets manager em produção (v0.6.0)

```bash
# Pre-commit hook (futuro)
#!/bin/bash
if git diff --cached --name-only | grep -q "^\.env$"; then
    echo "ERROR: .env file should not be committed!"
    exit 1
fi
```

**Prioridade**: Crítica (v0.6.0)  
**Workaround**: Revisar PRs manualmente

---

## 🟠 Alto

### 4. Dados Mockados (Não Integra com API Real)

**Descrição**: `ItemService` usa dados mockados em vez de chamar API externa.

**Impacto**:
- ⚠️ Não testa integração real
- ⚠️ Dados não persistem
- ⚠️ Limitado para demonstração

**Localização**: `app/services/item_service.py`

**Solução**: Ver [INTEGRATIONS.md](INTEGRATIONS.md) - Migração de Mock para Real

**Prioridade**: Alta (quando API real disponível)  
**Workaround**: Aceitável para desenvolvimento

---

### 5. Sem Rate Limiting

**Descrição**: Aplicação não limita taxa de requisições.

**Impacto**:
- ⚠️ Vulnerável a abuse/DoS
- ⚠️ Pode sobrecarregar API externa
- ⚠️ Custos descontrolados

**Localização**: N/A (não implementado)

**Solução proposta**:
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/items")
@limiter.limit("100/minute")
async def get_items():
    ...
```

**Prioridade**: Alta (v0.2.0)  
**Workaround**: Rate limiting no API Gateway/Load Balancer

---

### 6. Sem Circuit Breaker

**Descrição**: Não há circuit breaker para API externa.

**Impacto**:
- ⚠️ Cascading failures
- ⚠️ Recursos desperdiçados em API indisponível
- ⚠️ Latência alta quando API está lenta

**Localização**: `app/clients/api_client.py`

**Solução proposta**:
```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
async def get_data(self, endpoint: str) -> dict:
    ...
```

**Prioridade**: Alta (v0.2.0)  
**Workaround**: Timeout configurável (já implementado)

---

## 🟡 Médio

### 7. Cobertura de Testes Abaixo da Meta

**Descrição**: Cobertura atual ~70%, meta >80%.

**Impacto**:
- ⚠️ Bugs podem passar despercebidos
- ⚠️ Refatoração mais arriscada

**Localização**: `tests/`

**Gaps principais**:
- Validação de Pydantic models (~50%)
- Error handling em endpoints
- Edge cases

**Solução**: Ver [TESTING.md](TESTING.md) - Gaps de Teste

**Prioridade**: Média (incremental)

---

### 8. Logging Não Estruturado

**Descrição**: Logs são texto simples, não JSON.

**Impacto**:
- ⚠️ Difícil de parsear/agregar
- ⚠️ Sem correlation IDs
- ⚠️ Não integra bem com ferramentas de log aggregation

**Localização**: `main.py` (linha ~20)

**Solução proposta**:
```python
import structlog

logger = structlog.get_logger()
logger.info("processing_request", item_id=item_id, user_id=user_id)
```

**Prioridade**: Média (v0.4.0)

---

### 9. Sem Paginação

**Descrição**: Endpoint `GET /items` retorna todos os items.

**Impacto**:
- ⚠️ Performance ruim com muitos items
- ⚠️ Payload grande
- ⚠️ Timeout em listas grandes

**Localização**: `app/api/routes/items.py`

**Solução proposta**:
```python
@router.get("/items")
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    return await service.get_items(skip=skip, limit=limit)
```

**Prioridade**: Média (v0.3.0)

---

### 10. Sem Filtros e Ordenação

**Descrição**: Não é possível filtrar ou ordenar items.

**Impacto**:
- ⚠️ Cliente precisa filtrar localmente
- ⚠️ Tráfego desnecessário
- ⚠️ UX ruim

**Localização**: `app/api/routes/items.py`

**Solução proposta**:
```python
@router.get("/items")
async def get_items(
    name: Optional[str] = None,
    sort_by: Optional[str] = Query(None, regex="^(name|created_at)$"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$")
):
    return await service.get_items(
        filters={"name": name},
        sort_by=sort_by,
        order=order
    )
```

**Prioridade**: Média (v0.3.0)

---

## 🟢 Baixo

### 11. Type Checking Não Automatizado

**Descrição**: `mypy` não roda em CI.

**Impacto**:
- ℹ️ Type errors podem passar despercebidos
- ℹ️ Confiança menor em type hints

**Solução**: Adicionar mypy ao CI (v0.5.0)

**Prioridade**: Baixa

---

### 12. Sem Compressão de Respostas

**Descrição**: Respostas HTTP não são comprimidas (gzip).

**Impacto**:
- ℹ️ Payloads maiores
- ℹ️ Latência ligeiramente maior

**Solução**:
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**Prioridade**: Baixa (v0.3.0)

---

### 13. Sem Métricas

**Descrição**: Não há coleta de métricas (latência, taxa de erro, etc.).

**Impacto**:
- ℹ️ Difícil de monitorar performance
- ℹ️ Não há visibilidade de problemas

**Solução**: Prometheus + Grafana (v0.4.0)

**Prioridade**: Baixa (v0.4.0)

---

### 14. Sem Containerização

**Descrição**: Aplicação não tem Dockerfile.

**Impacto**:
- ℹ️ Deploy manual
- ℹ️ Inconsistência entre ambientes

**Solução**: Dockerfile multi-stage (v0.5.0)

**Prioridade**: Baixa (v0.5.0)

---

## 📊 Resumo de Prioridades

| Prioridade | Count | Items |
|------------|-------|-------|
| 🔴 Crítico | 3 | #1, #2, #3 |
| 🟠 Alto | 4 | #4, #5, #6, #7 |
| 🟡 Médio | 3 | #8, #9, #10 |
| 🟢 Baixo | 4 | #11, #12, #13, #14 |

---

## 🔍 Áreas Frágeis

### `app/core/auth.py`

**Fragilidade**: Alta

**Razões**:
- Token em memória (não persiste)
- Não suporta multi-instância
- Sem testes de concorrência

**Cuidados ao modificar**:
- Testar expiração de token
- Testar renovação automática
- Considerar race conditions

---

### `app/clients/api_client.py`

**Fragilidade**: Média

**Razões**:
- Sem retry logic
- Sem circuit breaker
- Error handling básico

**Cuidados ao modificar**:
- Testar timeouts
- Testar error handling
- Não quebrar injeção de JWT

---

### `app/services/item_service.py`

**Fragilidade**: Baixa

**Razões**:
- Dados mockados (fácil de testar)
- Lógica simples

**Cuidados ao modificar**:
- Manter interface consistente
- Atualizar testes quando migrar para API real

---

## 📝 Tech Debt Log

### [2026-03-22] Dados Mockados

**Razão**: API externa não disponível no momento.

**Impacto**: Limitado para demonstração.

**Plano**: Migrar quando API real estiver disponível.

---

### [2026-03-22] JWT em Memória

**Razão**: Simplicidade para v0.1.0.

**Impacto**: Não funciona em multi-instância.

**Plano**: Redis cache em v0.3.0.

---

## 🎯 Ações Recomendadas

### Curto Prazo (v0.2.0)

1. ✅ Implementar retry logic
2. ✅ Implementar circuit breaker
3. ✅ Adicionar rate limiting
4. ✅ Melhorar cobertura de testes

### Médio Prazo (v0.3.0 - v0.4.0)

1. ✅ Redis cache para JWT
2. ✅ Paginação e filtros
3. ✅ Structured logging
4. ✅ Métricas (Prometheus)

### Longo Prazo (v0.5.0+)

1. ✅ Containerização
2. ✅ CI/CD pipeline
3. ✅ Secrets management
4. ✅ Pre-commit hooks

---

## 📚 Referências

- [ROADMAP.md](../project/ROADMAP.md) - Features planejadas
- [STATE.md](../project/STATE.md) - Decisões e blockers
- [TESTING.md](TESTING.md) - Gaps de teste
- [INTEGRATIONS.md](INTEGRATIONS.md) - Integrações externas
