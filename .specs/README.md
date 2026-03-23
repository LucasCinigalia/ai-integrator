# .specs/ - Especificações e Documentação do Projeto

Esta pasta contém toda a documentação estruturada do projeto, seguindo o padrão **tlc-spec-driven**.

---

## 📁 Estrutura

```
.specs/
├── project/         # Documentos de projeto (visão, roadmap, estado)
├── codebase/        # Análise técnica do codebase
├── features/        # Especificações de features
└── quick/           # Tasks rápidas (ad-hoc)
```

---

## 📂 project/ - Documentos de Projeto

Documentação de alto nível sobre visão, objetivos e estado do projeto.

### Arquivos

| Arquivo | Descrição | Quando Ler |
|---------|-----------|------------|
| **PROJECT.md** | Visão, objetivos, princípios, stakeholders | Entender o projeto |
| **ROADMAP.md** | Features planejadas, milestones | Planejar trabalho |
| **STATE.md** | Estado atual, decisões, TODOs, lições | Sempre, antes de trabalhar |

### PROJECT.md

**Conteúdo**:
- Visão geral do projeto
- Objetivos (principal e específicos)
- Escopo (dentro e fora)
- Stakeholders
- Princípios de design
- Tecnologias core
- Métricas de sucesso
- Riscos e mitigações

**Quando atualizar**: Mudanças de visão, novos objetivos, novos stakeholders.

---

### ROADMAP.md

**Conteúdo**:
- Status atual (versão)
- Features implementadas
- Milestones futuros (v0.2.0, v0.3.0, etc.)
- Features planejadas por milestone
- Backlog (features sem milestone)

**Quando atualizar**: Nova feature planejada, milestone concluído, prioridades mudaram.

---

### STATE.md

**Conteúdo**:
- Status atual (versão, fase, branch)
- TODOs ativos (prioridade alta/média/baixa)
- Decisões arquiteturais (log de decisões)
- Blockers ativos e resolvidos
- Lições aprendidas
- Ideias deferidas
- Notas de sessão
- Preferências (modelos, ferramentas)

**Quando atualizar**: 
- Sempre que tomar decisão importante
- Sempre que adicionar/completar TODO
- Sempre que encontrar blocker
- Sempre que aprender algo importante
- No fim de cada sessão de trabalho

---

## 📂 codebase/ - Análise Técnica

Documentação técnica detalhada do codebase (brownfield analysis).

### Arquivos

| Arquivo | Descrição | Quando Ler |
|---------|-----------|------------|
| **STACK.md** | Stack tecnológica, dependências | Entender tecnologias |
| **ARCHITECTURE.md** | Arquitetura, camadas, padrões | Entender estrutura |
| **CONVENTIONS.md** | Convenções de código, estilo | Antes de escrever código |
| **STRUCTURE.md** | Estrutura de diretórios | Navegar no projeto |
| **TESTING.md** | Estratégia de testes | Escrever testes |
| **INTEGRATIONS.md** | Integrações externas | Trabalhar com APIs/libs |
| **CONCERNS.md** | Tech debt, riscos, áreas frágeis | Antes de modificar código |

### STACK.md

**Conteúdo**:
- Linguagem e runtime
- Frameworks e bibliotecas
- Dependências (principais e futuras)
- Decisões de stack (por quê cada tecnologia)
- Versões mínimas
- Compatibilidade

**Quando atualizar**: Nova dependência, upgrade de versão, nova tecnologia.

---

### ARCHITECTURE.md

**Conteúdo**:
- Visão geral da arquitetura
- Diagrama de camadas
- Fluxo de dados
- Detalhamento de cada camada
- Padrões de design aplicados
- Princípios (SOLID, Clean Architecture, 12-Factor)
- Escalabilidade
- Segurança
- Observabilidade

**Quando atualizar**: Mudança arquitetural, novo padrão, nova camada.

---

### CONVENTIONS.md

**Conteúdo**:
- Idioma (código, docs, commits)
- Python Style Guide (PEP 8)
- Nomenclatura (variáveis, classes, arquivos)
- Type hints
- Docstrings (Google Style)
- Imports
- Async/await
- Error handling
- Logging
- Pydantic models
- Testes
- Configuração
- Comentários
- Git commits

**Quando atualizar**: Nova convenção, mudança de padrão.

---

### STRUCTURE.md

**Conteúdo**:
- Visão geral da estrutura
- Detalhamento de diretórios
- Arquivos raiz
- Fluxo de arquivos
- Padrões de organização
- Como adicionar features/integrações/endpoints
- Arquivos gerados (não versionados)
- Métricas

**Quando atualizar**: Novo diretório, nova estrutura, reorganização.

---

### TESTING.md

**Conteúdo**:
- Pirâmide de testes (unit, integration, e2e)
- Estrutura de testes
- Arquivos de teste detalhados
- Padrões de teste (AAA, nomenclatura)
- Mocking
- Executando testes
- Configuração do pytest
- Cobertura de testes
- Gaps de teste (TODOs)
- CI/CD (futuro)
- Boas práticas

**Quando atualizar**: Novo tipo de teste, mudança de estratégia, novos gaps.

---

### INTEGRATIONS.md

**Conteúdo**:
- API externa (mock/real)
- Bibliotecas principais (FastAPI, httpx, Pydantic, etc.)
- Integrações futuras (Redis, Prometheus, etc.)
- Dependências de desenvolvimento
- Segurança (secrets management)
- Monitoring e observabilidade
- Rate limiting (futuro)

**Quando atualizar**: Nova integração, mudança de biblioteca, nova API.

---

### CONCERNS.md

**Conteúdo**:
- Concerns críticos (🔴)
- Concerns altos (🟠)
- Concerns médios (🟡)
- Concerns baixos (🟢)
- Resumo de prioridades
- Áreas frágeis (código sensível)
- Tech debt log
- Ações recomendadas (curto/médio/longo prazo)

**Quando atualizar**: 
- Novo tech debt identificado
- Concern resolvido
- Mudança de prioridade
- Nova área frágil

---

## 📂 features/ - Especificações de Features

Documentação de features específicas (grandes ou complexas).

### Estrutura

```
features/
└── [feature-name]/
    ├── spec.md      # Especificação (requisitos)
    ├── context.md   # Contexto e decisões de design
    ├── design.md    # Arquitetura da feature
    └── tasks.md     # Tasks atômicas
```

### Quando Criar

- **Large features**: Multi-componente, >10 tasks
- **Complex features**: Ambiguidade, decisões de design, novo domínio

### Quando NÃO Criar

- **Small features**: ≤3 arquivos, óbvio
- **Medium features**: Claro, <10 tasks (design inline)

### spec.md

**Conteúdo**:
- Visão geral da feature
- Requisitos funcionais (com IDs: REQ-001, REQ-002)
- Requisitos não-funcionais
- User stories
- Casos de uso
- Critérios de aceitação

---

### context.md

**Conteúdo**:
- Decisões de design (gray areas)
- Trade-offs considerados
- Alternativas descartadas
- Contexto do usuário

**Quando criar**: Apenas quando há ambiguidade ou múltiplas abordagens válidas.

---

### design.md

**Conteúdo**:
- Arquitetura da feature
- Componentes e suas responsabilidades
- Fluxo de dados
- Schemas (Pydantic models)
- Endpoints (se aplicável)
- Integrações externas

**Quando criar**: Features Large ou Complex (ver auto-sizing).

---

### tasks.md

**Conteúdo**:
- Lista de tasks atômicas
- Dependências entre tasks
- Critérios de verificação por task
- Status (pending, in_progress, completed)

**Quando criar**: Features Large ou Complex (ver auto-sizing).

---

## 📂 quick/ - Tasks Rápidas

Tasks ad-hoc, pequenas, que não justificam spec completa.

### Estrutura

```
quick/
└── NNN-slug/
    ├── TASK.md      # Descrição da task
    └── SUMMARY.md   # Resumo da execução
```

### Quando Usar

- **Bug fixes**: Correções rápidas
- **Config changes**: Ajustes de configuração
- **Small tweaks**: Mudanças ≤3 arquivos

### TASK.md

**Conteúdo**:
- Descrição da task
- Contexto
- Passos planejados

---

### SUMMARY.md

**Conteúdo**:
- O que foi feito
- Arquivos modificados
- Decisões tomadas
- Testes adicionados

---

## 🔄 Workflow

### Novo Projeto

1. Criar `project/PROJECT.md` (visão, objetivos)
2. Criar `project/ROADMAP.md` (features planejadas)
3. Criar `project/STATE.md` (estado inicial)

### Projeto Existente (Brownfield)

1. Mapear codebase → criar 7 docs em `codebase/`
2. Criar `project/PROJECT.md`
3. Criar `project/ROADMAP.md`
4. Criar `project/STATE.md`

### Nova Feature (Large/Complex)

1. Criar `features/[feature-name]/spec.md`
2. (Opcional) Criar `context.md` se houver ambiguidade
3. (Opcional) Criar `design.md` se complexo
4. (Opcional) Criar `tasks.md` se >5 tasks
5. Implementar
6. Atualizar `STATE.md` (decisões, lições)
7. Atualizar `ROADMAP.md` (marcar como concluído)

### Quick Task

1. Criar `quick/NNN-slug/TASK.md`
2. Implementar
3. Criar `quick/NNN-slug/SUMMARY.md`
4. Atualizar `STATE.md` se relevante

---

## 📖 Context Loading Strategy

### Base Load (~15k tokens)

**Sempre carregar**:
- `project/PROJECT.md`
- `project/ROADMAP.md`
- `project/STATE.md`

### On-Demand Load

**Carregar quando necessário**:
- `codebase/*` (quando trabalhando em código)
- `codebase/CONCERNS.md` (quando modificando áreas sensíveis)
- `features/[feature]/spec.md` (quando trabalhando na feature)
- `features/[feature]/design.md` (quando implementando)
- `features/[feature]/tasks.md` (quando executando tasks)

### NUNCA Carregar Simultaneamente

- ❌ Múltiplas specs de features
- ❌ Múltiplos docs de arquitetura
- ❌ Documentos arquivados

**Meta**: <40k tokens total context

---

## 🎯 Auto-Sizing de Features

| Scope | Specify | Design | Tasks | Execute |
|-------|---------|--------|-------|---------|
| **Small** (≤3 files) | Skip pipeline | - | - | - |
| **Medium** (<10 tasks) | Spec (brief) | Skip | Skip | Implement + verify |
| **Large** (multi-component) | Full spec | Architecture | Full breakdown | Implement + verify |
| **Complex** (ambiguity) | Full spec + discuss | Research + arch | Breakdown + parallel | Implement + UAT |

**Regra de ouro**: Specify e Execute são sempre necessários. Design e Tasks são opcionais baseados na complexidade.

---

## 📝 Manutenção

### Documentos Vivos

Estes documentos devem ser **sempre atualizados** junto com o código:

- ✅ `STATE.md` - Após cada decisão importante
- ✅ `CONCERNS.md` - Quando identificar tech debt
- ✅ `ROADMAP.md` - Quando planejar/concluir features
- ✅ `ARCHITECTURE.md` - Quando mudar arquitetura
- ✅ `CONVENTIONS.md` - Quando mudar padrões

### Documentos Estáticos

Estes documentos são criados uma vez e raramente mudam:

- `PROJECT.md` - Apenas se visão mudar
- `STACK.md` - Apenas se adicionar/remover tecnologia
- `STRUCTURE.md` - Apenas se reorganizar projeto

---

## 🔗 Integração com Outras Docs

### Relação com Docs Raiz

| Doc Raiz | Relação com .specs/ |
|----------|---------------------|
| **README.md** | Visão geral → `PROJECT.md` tem detalhes |
| **CONTRIBUTING.md** | Processo → `CONVENTIONS.md` tem padrões |
| **DOCS_STANDARD.md** | Padrão de docs → `.specs/` segue tlc-spec-driven |
| **AGENTS.md** | Regras → Referencia `.specs/` como fonte de verdade |

### Relação com docs/

| docs/ | Relação com .specs/ |
|-------|---------------------|
| **docs/architecture.md** | Visão geral → `codebase/ARCHITECTURE.md` tem detalhes |
| **docs/api.md** | Endpoints → `features/*/spec.md` tem requisitos |
| **docs/installation.md** | Como instalar → `codebase/STACK.md` tem dependências |

---

## 🎓 Referências

- [tlc-spec-driven skill](https://github.com/techleadersclub/tlc-spec-driven)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [docs-writer skill](https://github.com/cursor-community/docs-writer)

---

**Última atualização**: 2026-03-22
