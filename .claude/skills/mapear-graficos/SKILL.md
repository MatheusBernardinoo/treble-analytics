---
name: mapear-graficos
description: Aplica o de-para fixo de 10 gráficos, copia os PNGs para a pasta da semana com nomes numerados na ordem do relatório e valida tamanho > 0 de cada um. Não confiar na numeração interna do script; usar o nome do arquivo. Usado pelo Cientista.
allowed-tools: Bash, Read
---

# mapear-graficos

O script gera mais de 15 PNGs, mas **só 10 entram no relatório semanal e 11 no de período** (6 seções; as seções 02, 03, 05 e 06 têm 2 gráficos cada; no período a S.04 também tem 2, com o `D3_tempo_semanal`). O modelo é fixo — os dados e o período variam, mas a estrutura de seções e gráficos não muda.

## De-para fixo (use o NOME do arquivo, não a numeração interna)
| # | Indicador (seção) | Arquivo em `graficos/treble/` |
|---|---|---|
| 01 | Conversas: respondidas x sem resposta (S.01) | `A1_resposta.png` |
| 02a | Chegada ao vendedor x conversas atendidas — absoluto, barras sobrepostas (S.02) | SEMANAL: `B_24h_dia.png` (diário seg–sex) · PERÍODO: `B_24h.png` |
| 02b | Conversas atendidas — proporcional, empilhado % (S.02) | SEMANAL: `B_24h_dia_stacked.png` · PERÍODO: `B_24h_stacked.png` |
| 03a | Conversas recebidas por vendedor (S.03) | `D1_recebidos.png` |
| 03b | % de conversas respondidas por vendedor (S.03) | `D2_resp.png` |
| 04a | Tempo mediano de 1ª resposta — evolução semanal do time, linha única (S.04) | **SÓ PERÍODO:** `D3_tempo_semanal.png` (não existe no relatório semanal) |
| 04b | Tempo mediano de 1ª resposta (h) — resumo (S.04) | `D4_tempo.png` |
| 05a | Composição por padrão de resíduo, pizza (S.05) | `R1_residuo_comp.png` |
| 05b | Respondidos x sem resposta por padrão (S.05) | `R2_residuo_resp.png` |
| 06a | Completude, Sou novo por aqui (S.06) | `G2b_novo.png` |
| 06b | Completude, Já sou cliente (S.06) | `G2c_cli.png` |

## FORA do escopo (não repassar)
B (linha %), a variante de cadência não usada pelo tipo (semanal descarta `B_24h.png`/`B_24h_stacked.png`; período descarta `B_24h_dia*.png`), `D3_taxa_resp_tempo.png`, `D3_24h.png`, `D5_finish_vend.png`, `D6_sender_vend.png`, `D7_transfer.png`, `C1_retorno.png`, `E1_inbox.png`, `F1_status.png`, `F2_funil.png`, `F3_tend.png`, `G3_estado.png`. Em especial: transferências por vendedor, conversas por estado, destino das sessões, volume diário/taxa de repasse, SLA 72h, AUTO × MANUAL, "quem enviou a última mensagem".

## Procedimento
1. Copiar os 10 arquivos para a pasta da semana com nomes estáveis e numerados na ordem da tabela (`01_*.png` … `06b_*.png`).
2. Validar que os 10 caminhos existem e têm **tamanho > 0**.
3. Montar o manifesto `[GRÁFICOS]` associando cada arquivo ao indicador e à seção.

## Regra
- Não editar as imagens (não recortar, não regenerar). Apenas copiar e mapear.
- Se algum faltar ou estiver vazio (ex.: semana sem industriais pode reduzir as fatias do 06a/05a), registrar em `[ALERTAS]` indicando qual, não substituir por outro gráfico.
