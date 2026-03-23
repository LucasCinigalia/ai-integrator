# Padrão de Documentação do API Integrator

Este documento define o padrão de documentação do projeto, alinhado às diretrizes do **docs-writer**. Qualquer criação ou edição de documentação deve seguir estas regras.

## Arquivos de referência

| Arquivo | Descrição |
|---------|-----------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Processo de contribuição para documentação |
| [references/style-guide.md](references/style-guide.md) | Guia de estilo (tom, formatação, terminologia) |
| [docs/sidebar.json](docs/sidebar.json) | Navegação da documentação |

## Fluxo do docs-writer (4 passos)

### 1. Entender o objetivo e criar um plano

- Esclarecer a solicitação: qual recurso, comando ou conceito precisa de documentação?
- Diferenciar: é **escrita** de conteúdo novo ou **edição** de existente?
- Formular plano claro e passo a passo.

### 2. Investigar e reunir informações

- **Ler o código:** examinar `app/` para garantir que a docs reflita a implementação.
- **Identificar arquivos:** localizar em `docs/` ou `references/` o que será alterado.
- **Verificar conexões:** atualizar `docs/sidebar.json` se adicionar página nova; manter links válidos.

### 3. Escrever ou editar

- Seguir o [guia de estilo](references/style-guide.md).
- Garantir precisão em relação ao código.
- Edições pequenas: `replace`. Edições grandes/novos arquivos: `write`.

**Ao editar:**

- Corrigir lacunas (conteúdo incompleto ou desatualizado).
- Usar tom ativo e envolvente.
- Melhorar clareza (ortografia, gramática, frases).
- Manter consistência de terminologia e estilo.

### 4. Verificar e finalizar

- Revisar arquivos alterados (formatação e precisão).
- Verificar todos os links (novos e que referenciam o conteúdo alterado).
- Executar formatação e checagem:

```bash
ruff format .
ruff check .
```

## Estrutura da documentação

```
ai-integrator/
├── README.md                 # Visão geral do projeto
├── CONTRIBUTING.md           # Processo de contribuição
├── DOCS_STANDARD.md          # Este arquivo
├── docs/                     # Documentação técnica
│   ├── index.md              # Índice da documentação
│   ├── sidebar.json          # Navegação
│   ├── installation.md       # Guia de instalação
│   ├── api.md                # Endpoints da API
│   └── architecture.md       # Arquitetura e decisões
└── references/               # Referências e guias
    └── style-guide.md        # Guia de estilo
```

## Princípios obrigatórios

1. **Precisão:** a documentação reflete o código atual.
2. **Clareza:** escrita direta e fácil de entender.
3. **Consistência:** mesma terminologia e estilo em todos os documentos.
4. **Tom ativo:** voz ativa em vez de passiva.
5. **Links válidos:** verificar links antes de commitar.

## Checklist antes de commitar alterações em docs

- [ ] Leitura do [guia de estilo](references/style-guide.md)
- [ ] Documentação alinhada ao código em `app/`
- [ ] `docs/sidebar.json` atualizado se adicionou nova página
- [ ] Links verificados
- [ ] `ruff format .` e `ruff check .` executados
