---
name: montar-pacote-de-dados
description: Extrai os números das abas indicadas do relatorio_treble_semanal.xlsx e monta o PACOTE DE DADOS no formato padrão (única saída do Cientista para o Redator). Fonte única são as abas do xlsx; nunca recalcular por fora.
allowed-tools: Bash, Read
---

# montar-pacote-de-dados

## Fonte única (abas do `relatorio_treble_semanal.xlsx`)
| Bloco | Aba de origem | Colunas-chave |
|---|---|---|
| Atendimento (totais) | `A1_resumo` | Métrica, Valor |
| Por vendedor | `D1_por_vendedor` | vendedor, chats_recebidos, respondidos, %_nao_respondidos, %_em_24h, tempo_med_1a_resp_h |
| 24h por dia | `B_24h_diario` | dia, chegaram, respondidos_24h — base da S.02 DIÁRIA (seg–sex) do relatório semanal |
| Padrão resíduo (composição) | `R1_residuo_comp` | padrao, contatos, % |
| Padrão resíduo (resposta) | `R2_residuo_resp` | padrao, contatos, respondidos, sem_resposta, %_sem_resposta, %_respondida |
| Caminhos do fluxo | `G1_caminhos` | caminho, conversas, % |
| Completude | `G2b_completude_novo` / `G2c_completude_cli` | campo, preenchidos, %_preenchido — linhas já na ORDEM REAL do fluxo (1ª pergunta primeiro); `G2_completude` é auxiliar |

Notas de semântica (06/07/2026):
- Transferências na `D1_por_vendedor`: `transferiu_out` = quem ORIGINOU (last_transfer_from); `recebidos_via_transfer` = conversa do vendedor com transferência originada por outro. Fora do relatório, mas usadas em consultas internas.
- Gráficos de % por vendedor excluem quem tem 0 recebidas.

## Formato do PACOTE DE DADOS (preencher com valores reais, manter rótulos)
```
PACOTE DE DADOS, SEMANA {INICIO} a {FIM}

[METADADOS]
- Período: {INICIO} (dom) a {FIM} (sáb)
- Gerado em: {DATA_HORA}
- Arquivo de origem: {nome}
- Versões do fluxo detectadas: {n}
- Execução: OK | com alertas

[ATENDIMENTO, base: atendimento-treble]
- Conversas atribuídas: {n}
- Respondidas / Sem resposta: {n} / {n}  (% sem resposta: {x}%)
- Conversas atendidas: {n}
- Tempo mediano de 1ª resposta (h): {x}

[POR VENDEDOR]  (ordenar por conversas recebidas, desc)
vendedor | recebidas | respondidas | % sem resposta | % atendidas | tempo med 1a resp (h)
... uma linha por vendedor canônico ...

[24h POR DIA]  (números absolutos)
dia | chegaram ao vendedor | conversas atendidas

[PADRÃO DE RESÍDUO, contatos atribuídos x classe do fluxo]
padrao | contatos | % | % sem resposta | % respondida

[FLUXO]
- Sessões no período: {n}  | Contatos únicos: {n}
- Caminhos: novo {x}% | cliente {x}% | indeterminado {x}%

[COMPLETUDE]
- Completude (campo: % preenchido): {...}  (CPF e CNPJ unificados em cpf/cnpj)

[ARTEFATOS]
- Planilha: {caminho}/relatorio_treble_semanal.xlsx (00_PAINEL com gráficos)
- Origem das imagens: PNGs de graficos/treble/ | extraídas do 00_PAINEL (fallback)

[GRÁFICOS — 10 arquivos (semanal) / 11 (período, +D3_tempo_semanal) para o Redator]
01  Conversas: respondidas x sem resposta                  -> {caminho}/01_*.png    (S.01)
02a Chegada x conversas atendidas (absoluto) — semanal usa B_24h_dia.png (DIÁRIO seg–sex); período usa B_24h.png   (S.02)
02b Conversas atendidas — proporcional (%) — semanal usa B_24h_dia_stacked.png; período usa B_24h_stacked.png      (S.02)
03a Conversas recebidas por vendedor                       -> {caminho}/03a_*.png   (S.03)
03b % de conversas respondidas por vendedor                -> {caminho}/03b_*.png   (S.03)
04a Tempo mediano de 1ª resposta — evolução semanal do time (linha única) -> {caminho}/D3_tempo_semanal.png  (S.04, SÓ período)
04b Tempo mediano de 1ª resposta (h) — resumo              -> {caminho}/04_*.png    (S.04)
05a Composição por padrão de resíduo (pizza)               -> {caminho}/05a_*.png   (S.05)
05b Respondidos x sem resposta por padrão                  -> {caminho}/05b_*.png   (S.05)
06a Completude, Sou novo por aqui                          -> {caminho}/06a_*.png   (S.06)
06b Completude, Já sou cliente                             -> {caminho}/06b_*.png   (S.06)

[ALERTAS]
- {anomalias / sanity checks que falharam; nenhum se tudo ok}
```

## Sanity checks (apenas sinalizar em [ALERTAS], não corrigir em silêncio)
- A janela bate com domingo a sábado anteriores?
- Total de conversas e sessões é plausível (> 0, sem explosão atípica)?
- Os 10 gráficos existem e não estão vazios?
- Respondidas + Sem resposta = Total.

## Regras
- Os números vêm SEMPRE das abas do xlsx. Nunca recalcular por fora nem estimar. Faltou dado: "sem dados".
- Sem narrativa, adjetivos ou recomendações. Entregar só o pacote e repassar ao Redator.
- "Conversas respondidas x sem resposta" usa `atendimento-treble`; "SLA / sessões" usa o log de sessões. Bases distintas, não somar os dois totais.

## Fallback de imagens
Se `graficos/treble/` não existir, extrair as imagens embutidas do `00_PAINEL` abrindo o .xlsx como zip e lendo `xl/media/`, usando a POSIÇÃO/ORDEM das imagens na aba para mapear cada arquivo (não confiar na numeração de `xl/media/`).
