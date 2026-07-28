---
name: coletar-centro-de-metricas
description: No Centro de Métricas da Treble (app.treble.ai, conta Nexforce já logada via treble-login), reseta e seleciona o período da semana e dispara o download das métricas de sessões. SOMENTE LEITURA. Use após treble-login.
allowed-tools: mcp__claude-in-chrome, Read
---

# coletar-centro-de-metricas

Pré-requisito: sessão Nexforce aberta (skill `treble-login`). Use o período (domingo a sábado) informado pelo Supervisor.

## Procedimento
1. No menu lateral escuro à esquerda, acessar **"Centro de métricas"**.
2. No seletor de período (retângulo com a data + ícone de calendário), clicar para abrir o calendário.
3. Clicar em **"Resetar"** para limpar as datas preenchidas.
4. Selecionar o período: clicar primeiro no **domingo** (primeiro dia) e depois no **sábado** (último dia) da janela.
   - Ex.: janela 07/06/2026 a 13/06/2026 → clicar em 07/06 e depois em 13/06.
5. Clicar em **"Baixar métricas"**.

## Comportamento do download (confirmado em 25/06/2026)

- Após clicar em "Baixar métricas", o download pode ser imediato (arquivo cai em Downloads) **ou** assíncrono (aparece no Centro de Downloads como "Geral relatório").
- Se nenhum arquivo aparecer em Downloads em ~10 segundos, verificar no **Centro de Downloads** (ícone ↓ badge no header de `app.treble.ai/pt/dashboard/conversations`).
- No Centro de Downloads, o arquivo de sessões aparece com o label **"Geral relatório"** (diferente dos relatórios de versão do fluxo, que aparecem como "Relatório geral").

## Saída
- `general_sessions_report_AAAA_MM_DD_HH_MM_SS.csv` (ou .xlsx). Não renomear de forma a perder a data e hora.

## Regras
- SOMENTE LEITURA: só selecionar período e baixar. Não alterar filtros salvos, não editar, não clicar em ações de configuração.
- Se não conseguir baixar, parar e acionar §17 via Supervisor.
