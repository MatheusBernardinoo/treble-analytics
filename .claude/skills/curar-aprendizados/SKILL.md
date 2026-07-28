---
name: curar-aprendizados
description: Aplica as regras anti-inchaço e decide o que da execução merece registro na memória (só entra o que se repetiu ou o que causou/quase causou falha). Primeiro passo do Consultor de Aprendizado no fim do ciclo.
allowed-tools: Read
---

# curar-aprendizados

## Entrada
Coletar o que aconteceu na execução: alertas do Cientista, ajustes feitos pelo Organizador, atritos de coleta relatados, retornos do Validador e qualquer falha acionada pelo protocolo de erro.

## Decisão (curadoria)
Só entra na memória o que:
- se repetiu (padrão), OU
- causou / quase causou uma falha real (armadilha).
O resto é descartado. Registro cru e duplicado vira ruído.

## Regras anti-inchaço (§5)
- **Sem duplicar**: se o aprendizado já existe, atualizar a data, não criar linha nova.
- **Datado**: toda entrada começa com `[AAAA-MM-DD]`.
- **Promoção por evidência**: só sobe para "Convenções confirmadas" após repetir em ≥2 execuções ou ser validado pelo Matheus.
- **Teto por seção**: ~15 itens; consolidar semelhantes se passar.
- **Sem dados sensíveis**: nunca telefones, nomes de contatos ou conteúdo de conversa. A memória fala de processo, não de pessoas.

## Saída
Lista do que registrar e em qual seção (convenção / padrão / armadilha / ajuste pendente), para a skill `atualizar-memoria`.
