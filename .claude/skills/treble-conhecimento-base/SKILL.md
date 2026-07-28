---
name: treble-conhecimento-base
description: Responde dúvidas sobre conceitos e telas da Treble usando o CLAUDE.md e o referencia/DICIONARIO_DADOS.md como fonte primária. Primeira resposta do Consultor da Treble, antes de recorrer à documentação oficial.
allowed-tools: Read, Grep, Glob
---

# treble-conhecimento-base

## Fontes (nesta ordem)
1. `CLAUDE.md` (contexto, roteamento, fontes de dados, glossário §13.6).
2. `referencia/DICIONARIO_DADOS.md` (referência de arquivos, abas e colunas).
3. `CLAUDE.md` (resumo operacional).

## Procedimento
1. Identificar a dúvida (navegação, significado de uma tela, onde fica um relatório, o que é "versão do fluxo", definição de métrica).
2. Responder com base nas fontes do projeto, de forma curta e factual, citando a seção/aba relevante.
3. Se a dúvida não for resolvida pelas fontes internas, encaminhar para a skill `treble-consulta-docs`.

## Regra
- Não inventar comportamento da plataforma. Se a base interna não cobre, dizer e passar para a consulta à documentação.
