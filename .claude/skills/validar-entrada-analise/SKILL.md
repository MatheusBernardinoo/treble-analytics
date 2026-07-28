---
name: validar-entrada-analise
description: Confere a existência do arquivo unificado e a presença das abas essenciais ANTES de rodar a análise. Se faltar aba essencial ou o arquivo estiver corrompido, PARA e reporta. Usado pelo Cientista após parametrizar.
allowed-tools: Bash, Read
---

# validar-entrada-analise

## Procedimento
1. Confirmar que o arquivo unificado existe no caminho de `ARQUIVO`.
2. Confirmar as abas essenciais:
   - `atendimento-treble` (**obrigatória**: base de verdade)
   - ao menos uma aba de **versão**
   - aba de **sessões**
```bash
python -c "import pandas as pd,sys; xl=pd.ExcelFile(sys.argv[1]); print(xl.sheet_names)" "analises/DD-MM-AAAA a DD-MM-AAAA (geral)/Dados_Treble_Semana.xlsx"
```
3. Conferir que o arquivo não está corrompido (abre sem erro).

## Regra
- Se faltar aba essencial ou o arquivo estiver corrompido: **PARAR** e acionar o protocolo de falha-e-avisa (§17), avisando qual aba faltou. Não adivinhar, não preencher.
