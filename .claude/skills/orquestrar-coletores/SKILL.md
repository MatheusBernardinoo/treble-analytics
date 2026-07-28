---
name: orquestrar-coletores
description: Dispara os três coletores em paralelo (Centro de Métricas, Fluxo/Versões, Inbox), monitora a conclusão de cada um e consolida o status da coleta. Usado pelo Supervisor após calcular a janela.
allowed-tools: Agent, Read
---

# orquestrar-coletores

## Procedimento
1. Disparar os três coletores **em paralelo** (uma única mensagem com três chamadas Agent), passando a cada um o mesmo período da janela:
   - `coletor-centro-metricas`
   - `coletor-fluxo-versoes`
   - `coletor-inbox`
2. Acompanhar o progresso de cada um e responder dúvidas de navegação (apoiando-se no `consultor-treble` quando necessário).
3. Ao final, confirmar que **cada** coletor disparou a geração/download dos relatórios.
4. Consolidar o status: o que cada coletor baixou e onde.
5. Sinalizar ao `organizador-dados` que pode começar.

## Regra
- Se algum coletor não concluir (login caiu, relatório não gerou) ou sair do escopo somente-leitura, acionar `guardrail-somente-leitura` e, se a coleta ficar comprometida, o protocolo de falha-e-avisa (§17).
