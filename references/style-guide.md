# Guia de Estilo para Documentação

Este guia define os padrões de escrita e formatação para toda a documentação do API Integrator.

## Princípios Gerais

- **Clareza:** Escreva de forma direta e compreensível.
- **Precisão:** A documentação deve refletir o comportamento real do código.
- **Consistência:** Use terminologia e formatação consistentes em todos os documentos.
- **Tom ativo:** Prefira voz ativa. Ex.: "O cliente envia a requisição" em vez de "A requisição é enviada pelo cliente".

## Estrutura de Documentos

### Cabeçalhos

- Use `#` (H1) apenas para o título principal do documento.
- Hierarquia: H1 → H2 → H3. Evite pular níveis.
- Use sentence case nos títulos (primeira letra maiúscula, resto minúscula, exceto nomes próprios).

### Parágrafos

- Um conceito por parágrafo.
- Mantenha parágrafos curtos (3–5 linhas).
- Evite blocos longos e densos.

### Listas

- Use listas quando enumerar 3 ou mais itens.
- Itens de lista começam com letra minúscula (exceto nomes próprios).
- Ponto final apenas se o item for uma frase completa.

## Terminologia

| Termo | Uso correto | Evitar |
|-------|-------------|--------|
| API | API (maiúsculo) | api |
| JWT | JWT (sigla) | jwt |
| endpoint | minúsculo | Endpoint |
| item/items | conforme o domínio | Item/Items no meio de frases |

## Formatação de Código

### Blocos de código

- Sempre indique a linguagem: ` ```python `, ` ```bash `, ` ```json `, ` ```http `.
- Para requisições HTTP (método + path + headers): use ` ```http `.
- Para comandos executáveis: use ` ```bash ` e inclua comandos completos.
- Para exemplos de API executáveis, use curl ou Python (httpx/requests).

### Código inline

- Use backticks para: nomes de variáveis, funções, classes, módulos, comandos.
- Ex.: "A função `get_items()` retorna uma lista."

## Links

- Use links descritivos: "Consulte o [guia de instalação](docs/installation.md)" em vez de "Clique [aqui](docs/installation.md)".
- Verifique que os links estão funcionando antes de commitar.

## Exemplos e Snippets

- Exemplos devem ser válidos e seguir o estilo do projeto (ruff).
- Comentários em português nos exemplos.
- Inclua exemplos de sucesso e, quando relevante, de erro.

## Referências ao Código

- Ao citar um arquivo: `app/api/routes/items.py`
- Ao citar uma classe/função: `ExternalAPIClient`, `get_items`
- Mantenha referências alinhadas com o código atual.

## Formatação Markdown

- Uma linha em branco entre seções.
- Espaço após `-` ou `*` em listas.
- Tabelas com pipes alinhados para melhor leitura no código-fonte.

## Checklist antes de commitar

- [ ] Documentação reflete o código atual
- [ ] Guia de estilo foi seguido
- [ ] Links validados
- [ ] Exemplos testados
- [ ] `ruff format .` e `ruff check .` executados
