---
name: unificar-xlsx-semana
description: Roda scripts/geral/unificar_arquivos.py em modo automático sobre a pasta da semana e valida que as abas essenciais foram escritas (atendimento, sessões, ao menos uma versão). O número de versões é detectado sozinho. Último passo do Organizador.
allowed-tools: Bash, Read
---

# unificar-xlsx-semana

## Procedimento

1. Rodar o unificador a partir da **raiz do projeto** (não de dentro da pasta da semana), passando o caminho da pasta como argumento.
   ```bash
   # Rodar da raiz do projeto
   python scripts/geral/unificar_arquivos.py "analises/07-06-2026 a 13-06-2026 (geral)"
   ```
   O script grava `Dados_Treble_Semana.xlsx` no **diretório de trabalho atual** (raiz do projeto), não dentro da pasta da semana.

2. Mover o arquivo gerado para dentro da pasta da semana:
   ```bash
   mv Dados_Treble_Semana.xlsx "analises/07-06-2026 a 13-06-2026 (geral)"/
   ```
   Ou em PowerShell:
   ```powershell
   Move-Item Dados_Treble_Semana.xlsx "analises\07-06-2026 a 13-06-2026 (geral)\"
   ```

3. Conferir a saída do script: abas gravadas e nº de versões. O script alerta se faltar atendimento, sessões ou versão.

## Saída real do script
- **`Dados_Treble_Semana.xlsx`** (constante `ARQUIVO_SAIDA` do script), gravado na pasta de onde o python roda.
- Nota de adaptação: o CLAUDE.md cita o nome `Dados Treble Cliente - [período].xlsx`, mas o `/` é ilegal no Windows. O nome de trabalho é `Dados_Treble_Semana.xlsx`. O Cientista aponta `ARQUIVO` para esse arquivo. Se preferir um nome amigável, renomeie para `Dados Treble Cliente - [período].xlsx` (sem barra) e aponte o Cientista para ele.

## Abas resultantes
`atendimento-treble` · `sessoes-gerais` · `Versao 1` · `Versao 2` (…) · `inbox` (se houver). O script de análise classifica pelas COLUNAS, não pelo nome da aba.

## Validação obrigatória (antes de passar ao Cientista)
- Existe a aba de **atendimento** (base de verdade)?
- Existe a aba de **sessões**?
- Existe **ao menos uma versão**?
Se faltar alguma essencial, parar e acionar §17 (não improvisar).

## Fallback manual
- Se algum arquivo tiver nome muito fora do padrão e não for classificado, preencher `FONTES_MANUAIS` no fim do script e rodar com `--manual`.
