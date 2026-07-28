---
name: coletar-inbox-vendas
description: No Treble Sales (sales.treble.ai, conta do cliente já logada via treble-sales-login), acessa Administração, define o período da semana e dispara o download do relatório de atendimento por vendedor (base de verdade). SOMENTE LEITURA.
allowed-tools: mcp__claude-in-chrome, Read
---

# coletar-inbox-vendas

Pré-requisito: sessão do cliente aberta (skill `treble-sales-login`). Use o período informado pelo Supervisor.

## Procedimento

1. No menu lateral escuro, acessar **"Administração"**.
   - O item "Administração" fica em **y≈258** no viewport (1568×705). Atenção: y≈208 acerta "Contacts", que está acima. Confirmar com screenshot antes de clicar se houver dúvida.
2. Clicar no ícone de calendário com o texto **"Data de início → Data final"**.
3. Selecionar primeiro o **domingo** (primeiro dia) e depois o **sábado** (último dia) da semana anterior.
4. Clicar em **"Download"**.

## Comportamento do download (direto — confirmado em 25/06/2026)

- Este download é **direto**: o arquivo cai imediatamente em Downloads assim que o botão é clicado. Não passa pelo Centro de Downloads do `app.treble.ai`.
- Nome do arquivo: `treble (N).csv` (Chrome adiciona numeração automática se já houver um `treble.csv`).
- **NÃO confundir com os arquivos NX 01 (XLSX)** que vêm pelo Centro de Downloads.

## Saída
- `treble (N).csv`, contendo a aba interna `treble (2)`. É essa aba que vira `atendimento-treble` no arquivo unificado.

## Regras
- SOMENTE LEITURA: apenas definir período e baixar. Não editar, não alterar configuração.
- **Navegar SOMENTE por cliques na SPA (06/07/2026):** qualquer navegação direta por URL (navigate/F5/refresh) neste domínio retorna 500 e derruba a sessão — o login teria que ser refeito pelo operador. Chegar à Administração clicando na sidebar.
- Se não conseguir baixar, parar e acionar §17 via Supervisor.
