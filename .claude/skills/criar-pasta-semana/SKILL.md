---
name: criar-pasta-semana
description: Cria, dentro de analises/, a pasta da semana no padrão DD-MM-AAAA a DD-MM-AAAA (geral) e move para ela todos os arquivos baixados da execução. Usado pelo Organizador.
allowed-tools: Bash, Read
---

# criar-pasta-semana

## Procedimento

1. Criar a pasta da semana dentro de `analises/`, com o sufixo `(geral)`: `analises/DD-MM-AAAA a DD-MM-AAAA (geral)` (ex.: `analises/07-06-2026 a 13-06-2026 (geral)`), com os valores reais da janela.
2. **Verificar duplicatas entre os XLSX de versão antes de mover** (ver seção abaixo).
3. Mover para essa pasta todos os arquivos baixados no passo de download (sessões, versão(ões), atendimento).

```bash
# exemplo (Git Bash); ajuste o período e o caminho de Downloads
DEST="analises/07-06-2026 a 13-06-2026 (geral)"
mkdir -p "$DEST"
mv ~/Downloads/general_sessions_report_* "$DEST"/ 2>/dev/null
mv ~/Downloads/NX\ 01* "$DEST"/ 2>/dev/null
mv ~/Downloads/*reble* "$DEST"/ 2>/dev/null
```

## Deduplicação de XLSX (confirmado necessário em 25/06/2026)

O Chrome pode baixar o mesmo relatório duas vezes com nomes diferentes (ex.: `(14).xlsx` e `(17).xlsx` com conteúdo idêntico). Antes de mover, checar duplicatas por hash MD5:

```bash
# PowerShell — listar MD5 dos XLSX de versão
Get-FileHash ~/Downloads/"NX 01"*.xlsx -Algorithm MD5 | Select-Object Hash, Path | Sort-Object Hash
```

Se dois arquivos tiverem o mesmo Hash, manter apenas um e registrar no log. O script `unificar_arquivos.py` não detecta duplicatas — arquivos idênticos geram abas duplicadas e distorcem a análise.

## Regra
- Conferir que TODOS os arquivos da execução foram movidos antes de seguir para a unificação (incluindo TODAS as versões únicas).
- O `/` do nome aspiracional "Dados Treble Cliente" é ilegal em nomes de arquivo no Windows; a pasta usa só o período.
