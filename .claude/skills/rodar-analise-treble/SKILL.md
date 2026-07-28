---
name: rodar-analise-treble
description: Executa scripts/geral/analise_treble_semanal.py e confirma as saídas (relatorio_treble_semanal.xlsx com aba 00_PAINEL + abas analíticas, e os PNGs em graficos/treble/). Usado pelo Cientista após validar a entrada.
allowed-tools: Bash, Read
---

# rodar-analise-treble

## Procedimento
1. Executar o script:
   ```bash
   python scripts/geral/analise_treble_semanal.py
   ```
   O script já trata encoding (mojibake), telefone por núcleo nacional (ignora o 55), exclusão de telefones de teste e canonização de nomes de vendedores. **Não refazer isso à mão.**
2. Registrar o intervalo que o script reportar (linha "Janela analisada").
3. Confirmar as saídas:
   - `relatorio_treble_semanal.xlsx` (aba `00_PAINEL` + abas analíticas).
   - Pasta `graficos/treble/` com os PNGs.

## Regra
- Se a semana estiver vazia (0 conversas) ou a execução falhar: **PARAR** e acionar §17, avisando o motivo. Não estimar números.
