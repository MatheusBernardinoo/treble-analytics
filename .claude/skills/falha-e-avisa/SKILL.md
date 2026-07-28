---
name: falha-e-avisa
description: Reporta ao operador, no próprio chat, um aviso estruturado de falha quando o fluxo parou por erro. Acionado pelo Consultor de Aprendizado no fim do ciclo. Os agentes individuais nunca reportam para fora; eles param e reportam o erro para cima.
allowed-tools: Read
---

# falha-e-avisa

## Destinatário
O **operador**, no próprio chat da sessão. Este template não envia mensagens para fora (sem Slack, sem e-mail).

## Formato da mensagem
```
[FALHA — Automação Treble]

Janela-alvo: {período DD/MM a DD/MM}
Etapa: {coleta | organização | análise | redação | validação}
Agente: {nome do agente que parou}
O que aconteceu: {1 frase factual}
O que falta para resolver: {1 frase}
Status: fluxo interrompido, sem relatório gerado.
```

## Roteamento de falha
Os agentes individuais **não reportam para fora**. Eles PARAM e reportam o erro para o Supervisor ou orquestrador, que repassa ao Consultor de Aprendizado. O Consultor aciona este skill no fim do ciclo, consolidando o motivo da falha a partir do que os agentes reportaram.

## Regras
- Factual e curto. Descrever o evento, não culpar.
- Acionar antes de encerrar o ciclo, não depois.
- Nunca entregar relatório com dado incompleto ou suspeito.
