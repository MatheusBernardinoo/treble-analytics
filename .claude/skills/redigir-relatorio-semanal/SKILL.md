---
name: redigir-relatorio-semanal
description: Gera o relatório semanal em HTML com dark theme (capa escura, cards de KPI, gráficos em cards brancos, blocos de leitura). Script canônico: scripts/geral/gerar_relatorio_html.py. Saída: Relatório semanal Treble - [período].html
allowed-tools: Bash, Read, Write
---

# redigir-relatorio-semanal

## FORMATO: HTML (arquivo autocontido) — substituiu PDF em 30/06/2026

O relatório final é um **arquivo HTML autocontido**, com dark theme, idêntico ao design de `referencia/DESIGN.md`. As imagens são embutidas como base64 — o arquivo é autocontido e funciona offline.

## Implementação canônica: `scripts/geral/gerar_relatorio_html.py`

O relatório é gerado pelo script **`scripts/geral/gerar_relatorio_html.py`**. Sempre rodar a partir da **raiz do projeto**.

**Relatório semanal (entrega toda segunda-feira):**
```bash
python scripts/geral/gerar_relatorio_html.py
```

**Relatório de período (primeira segunda do mês):**
```bash
python scripts/geral/gerar_relatorio_html.py --tipo periodo
```

O script:
- Semanal: lê `relatorio_treble_semanal.xlsx` + `graficos/treble/` → `Relatório semanal Treble - [período].html`
- Periodo: lê `relatorio_equipe_periodo.xlsx` + `graficos/equipe/` → `Relatório Treble - Utilização geral - [período].html`
- Auto-detecta o período do xlsx (regex `DD-MM-AAAA a DD-MM-AAAA`); para semanal, fallback = semana anterior calculada dinamicamente
- Insere os 10 PNGs como base64 (S.02: `B_24h_dia.png` + `B_24h_dia_stacked.png` no semanal, `B_24h.png` + `B_24h_stacked.png` no período; mais 8 para as demais seções)

Requer apenas `openpyxl` (já instalado). Sem dependência de `reportlab`.

**Layout (baseado em `referencia/DESIGN.md`):** dark theme (`--bg: #000000`, `--surface: #111111`, `--accent: #1A6FFF`); fonte Lato (corpo) + JetBrains Mono (labels); gráficos em cards brancos; callouts com borda azul esquerda; tabela de resumo com linhas alternadas.

**Padrão canônico aprovado (03/07/2026, o responsável pelo cliente; atualizado em 06/07/2026):** o arquivo `o formato de referência do projeto` define o formato: **sem títulos cinza (captions) acima dos gráficos** (não passar `--com-titulos`), evolução semanal (S.04, só período) como linha única do time em horas (`--d3-unidade h`, o padrão), seção 06 com uma Leitura por gráfico, **sem informação equivalente repetida** (sem "% de atendimento realizado"; tabela de resíduo sem "% sem resposta"). Diferença por tipo: **S.02 é DIÁRIA seg–sex no semanal e SEMANAL no período**. O bloco `Iniciativa:` desse arquivo é exceção única; nenhum relatório novo tem Iniciativa.

## Estrutura (capa + 6 seções de conteúdo)
```
Capa: título, PERÍODO, FONTE (Treble · atendimento-treble), VOLUME ([N] conversas — sem contagem de sessões), RESPONSÁVEL (Nexforce · RevOps)
00: SUMÁRIO EXECUTIVO  (2 cards: % de conversas atendidas + tempo mediano; SEM "% de atendimento realizado" — regra absoluta de não repetir informação equivalente; "Maior % de resposta — vendedores" = os 3 maiores percentuais)
01: CONVERSAS: respondidas x sem resposta            (gráfico 01)
02: CONVERSAS ATENDIDAS: chegada x conversas atendidas (gráficos 02a absoluto sobreposto + 02b empilhado %; cadência DIÁRIA seg–sex no semanal, SEMANAL no relatório de período)
03: VOLUME POR VENDEDOR: conversas recebidas + % respondidas por vendedor (gráficos 03a D1_recebidos + 03b D2_resp)
04: TEMPO DE RESPOSTA: evolução semanal do time (linha única em horas, só período) + resumo por vendedor (gráficos 04a D3_tempo_semanal + 04b D4_tempo)
05: PADRÃO DE RESÍDUO: composição + respondidos x sem resposta (gráficos 05a, 05b)
06: QUALIFICAÇÃO: completude novo + completude cliente (gráficos 06a, 06b; UMA Leitura após cada gráfico, cruzamento dos fluxos na segunda)
Rodapé: Nexforce · RevOps
```

## Procedimento
1. Rodar `scripts/geral/gerar_relatorio_html.py` da raiz do projeto.
2. Confirmar que o arquivo `.html` foi gerado com tamanho razoável (> 500 KB).
3. Nomear `Relatório semanal Treble - [período].html` e repassar ao Validador.

## Regras inegociáveis
1. **Sem redundância**: cada número aparece UMA vez. Sumário traz só totais de volume; indicadores detalhados ficam nas seções.
2. **Sem meta nem interpretação**: nunca "meta", "objetivo", "ideal", "esperado". A `Leitura:` descreve o que o número é, nunca o que deveria ser.
3. **Sem sugestões (regra absoluta)**: nenhuma frase do relatório sugere ação ou mudança de processo. Só dados e relações sutis; interpretação é do cliente.
4. **Leituras cruzadas**: seção com 2+ gráficos exige `Leitura:` relacionando dados dos dois (regras completas no agente `redator-leituras`).

## Limites
- Sem recomendações nem juízo de valor sobre pessoas. Despersonalizar; o ponto de resíduo é apresentado de forma geral, sem apontar um vendedor.
