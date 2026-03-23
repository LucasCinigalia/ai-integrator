# Guia de Contribuição

Obrigado por contribuir com o API Integrator. Este documento descreve o processo para contribuir com **código** e **documentação**.

## Processo de Contribuição para Documentação

Todas as contribuições de documentação devem seguir o fluxo do **docs-writer**. Consulte também o [padrão de documentação](DOCS_STANDARD.md) para referência completa.

### 1. Entender o objetivo e criar um plano

1. **Esclarecer a solicitação:** Entenda completamente o pedido. Identifique o recurso, comando ou conceito central.
2. **Diferenciar a tarefa:** Determine se é **escrita** de conteúdo novo ou **edição** de conteúdo existente.
3. **Formular um plano:** Crie um plano claro e passo a passo para as alterações necessárias.

### 2. Investigar e reunir informações

1. **Ler o código:** Examine o código relevante em `app/` para garantir que a documentação reflita a implementação real.
2. **Identificar arquivos:** Localize os arquivos em `docs/` ou `references/` que precisam ser modificados.
3. **Verificar conexões:** Considere documentação relacionada. Atualize `docs/sidebar.json` se adicionar nova página. Mantenha links válidos.

### 3. Escrever ou editar a documentação

1. **Seguir o guia de estilo:** Siga as regras em `references/style-guide.md`.
2. **Precisão:** Garanta que a documentação reflita com precisão o código atual.
3. **Edições pequenas:** Use `replace`/`search_replace`. Edições grandes ou novos arquivos: use `write`.

### 4. Verificar e finalizar

1. **Revisar:** Leia novamente os arquivos alterados. Confira formatação e precisão.
2. **Verificar links:** Valide todos os links no conteúdo novo e nas páginas que referenciam o conteúdo alterado.
3. **Formatar:** Execute `ruff format` e `ruff check` para manter consistência.

```bash
ruff format .
ruff check .
```

## Como contribuir

1. Faça um fork do repositório
2. Crie uma branch para sua alteração (`git checkout -b feat/minha-contribuicao`)
3. Siga o guia de estilo e o processo de documentação acima
4. Commit suas alterações (`git commit -m 'feat: adiciona documentação X'`)
5. Push para a branch (`git push origin feat/minha-contribuicao`)
6. Abra um Pull Request

## Convenção de Commits

Utilize mensagens descritivas:

- `docs: adiciona guia de X`
- `docs: corrige descrição de Y`
- `feat: implementa Z`
- `fix: corrige bug em W`
