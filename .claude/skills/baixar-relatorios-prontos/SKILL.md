---
name: baixar-relatorios-prontos
description: No Centro de Downloads da Treble (app.treble.ai, conta Nexforce já logada), baixa todos os relatórios com "Gerado no dia" igual a hoje. SOMENTE LEITURA. Usado pelo Organizador após a espera de processamento.
allowed-tools: mcp__claude-in-chrome, Read
---

# baixar-relatorios-prontos

Pré-requisito: sessão Nexforce aberta (`treble-login`).

## Localização do Centro de Downloads (confirmado em 25/06/2026)

O Centro de Downloads NÃO está no menu lateral. É o **ícone ↓ (seta para baixo com badge numérico)** no canto superior direito do header, visível na página `app.treble.ai/pt/dashboard/conversations`. Clicar nesse ícone abre o painel "Centro de downloads" com o contador "Relatórios gerados X/Y".

**NÃO confundir com:**
- "Centro de métricas" (menu lateral) — é outra coisa
- A página de métricas de um fluxo específico — não tem os relatórios prontos

## Procedimento

1. Navegar para `app.treble.ai/pt/dashboard/conversations`.
2. Clicar no ícone ↓ (badge) no header superior direito.
3. No painel "Centro de downloads", verificar o contador "Relatórios gerados X/Y".
4. A lista está em **ordem cronológica decrescente** (mais recentes no topo).
5. Para cada entrada com **"Gerado no dia" = data de hoje**:
   - Clicar no ">" para expandir e confirmar o tipo ("Relatório geral" = versão do fluxo, XLSX; "Geral relatório" = sessões, CSV) e o período coberto.
   - Clicar em **"Baixar relatório"** e aguardar a mensagem de confirmação.
6. Repetir para todos os itens do dia.

## Identificar relatórios corretamente

- **NÃO usar o nome do arquivo** como identificador — todos os relatórios de versão têm nome idêntico ("NX 01. Fluxo conversacional WhatsApp (1235665) - Relatório geral").
- Usar **"Gerado no dia"** (data e hora) + **período exibido ao expandir** para distinguir versões entre si.
- Se duas entradas tiverem a mesma data/hora de geração, baixar ambas — o script de unificação lida com múltiplas versões.

## Arquivos esperados na pasta Downloads

- Sessões: `general_sessions_report_AAAA_MM_DD_HH_MM_SS.csv`
- Versões do fluxo: `NX 01. Fluxo conversacional WhatsApp (1235665) - Relatório geral (N).xlsx` (um por versão; Chrome numera automaticamente se o nome repetir)
- Atendimento o cliente: `treble (N).csv` — **esse arquivo NÃO vem do Centro de Downloads**; é baixado diretamente em sales.treble.ai › Administração (skill `coletar-inbox-vendas`).

## Relatórios ainda pendentes no contador

- Se o contador mostrar X/Y com X < Y, alguns relatórios ainda estão gerando.
- Aguardar conforme `espera-processamento-treble`. Se após 20 min ainda pendentes, prosseguir sem eles e registrar em `MEMORIA_APRENDIZADO.md`.
- Versões com poucos dados (ex.: 1 sessão) podem demorar mais ou travar; não bloquear o ciclo por elas.

## Regra
- SOMENTE LEITURA: baixar é leitura. Não clicar em editar, excluir ou reprocessar.
- Se algum arquivo não baixar, registrar e acionar §17 indicando qual faltou.
