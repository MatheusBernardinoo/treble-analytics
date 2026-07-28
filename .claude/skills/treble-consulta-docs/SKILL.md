---
name: treble-consulta-docs
description: Pesquisa em modo leitura na documentação oficial da Treble (help.treble.ai) quando a base interna não resolve a dúvida. Retorna a resposta resumida e o link da página consultada. SOMENTE LEITURA, nunca interage com a conta.
allowed-tools: WebFetch, WebSearch, Read
---

# treble-consulta-docs

## Quando usar
Só quando o `treble-conhecimento-base` não resolveu e a resposta é realmente necessária.

## Procedimento
1. Pesquisar na documentação oficial (help.treble.ai) o conceito ou tela em questão.
2. Ler em modo leitura; extrair a resposta.
3. Retornar: resposta resumida (2 a 4 linhas) + link da página consultada.

## Regras
- SOMENTE LEITURA. Mesmo na documentação, apenas consulta; nunca interage com a conta da Treble.
- Se a documentação não confirmar, responder "sem confirmação na documentação" e sugerir validar com o suporte. Não inventar.
