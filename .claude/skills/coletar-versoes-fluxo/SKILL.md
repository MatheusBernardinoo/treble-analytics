---
name: coletar-versoes-fluxo
description: Abre as métricas do fluxo NX 01 na Treble (app.treble.ai, conta Nexforce já logada), identifica TODAS as versões que cobrem o período (incluindo a mais próxima anterior ao primeiro dia) e baixa o relatório global XLSX de cada uma. SOMENTE LEITURA. Passo mais delicado da coleta.
allowed-tools: mcp__claude-in-chrome, Read
---

# coletar-versoes-fluxo

Pré-requisito: sessão Nexforce aberta (skill `treble-login`). Use o período informado pelo Supervisor.

## Procedimento
1. Acessar as métricas do fluxo **"NX 01..."** clicando no ícone de gráfico de barras (três barrinhas) ao lado do fluxo.
2. Localizar o seletor de versão (quadro com "Versão atual · data de lançamento · horário de lançamento").

## Lógica das versões (o ponto crítico)
- Baixar as métricas de **TODAS as versões que cobrem o período**.
- Regra: identificar a data do **primeiro dia da semana** e baixar todas as versões a partir da **mais próxima anterior a essa data, inclusive**. Isso garante cobertura total, mesmo que venham dados de antes da semana (o script descarta o que estiver fora da janela).
- Não assumir que há só uma versão; pode haver duas ou mais ativas (ex.: 71 e 72).

## Como disparar o download de cada versão

1. Selecionar a versão no seletor.
2. Clicar no botão preto **"Baixar relatório global"** (com ícone de download).
3. Selecionar o formato **XLSX** e clicar em **"Baixar relatório"**.
4. **O arquivo NÃO é baixado imediatamente.** O botão coloca a geração em fila assíncrona. O arquivo aparecerá no **Centro de Downloads** (ícone ↓ no header do dashboard) quando estiver pronto.
5. Repetir para cada versão necessária.

## Comportamento assíncrono (confirmado em 25/06/2026)

- Após clicar em "Baixar relatório", a plataforma exibe uma mensagem de confirmação mas o arquivo ainda não está disponível.
- O arquivo aparece no Centro de Downloads (ícone ↓ badge no header de `app.treble.ai/pt/dashboard/conversations`) sob o label **"Relatório geral"**, com um contador de progresso.
- O Organizador é responsável por aguardar e baixar os arquivos do Centro de Downloads (skill `baixar-relatorios-prontos`).
- Versões com dados escassos (ex.: 1 mensagem) podem ficar pendentes por >1h ou indefinidamente — não bloquear o ciclo por elas.

## Saída
- Os arquivos XLSX ficarão disponíveis no Centro de Downloads. O Organizador os baixa de lá.
- Nome no disco: `NX 01. Fluxo conversacional WhatsApp (1235665) - Relatório geral (N).xlsx` (Chrome adiciona numeração automática).

## Regras
- SOMENTE LEITURA: trocar de versão para visualizar/disparar download é leitura. Não editar versão, não publicar, não alterar o fluxo.
- Se não conseguir disparar o download, parar e acionar §17 via Supervisor.
