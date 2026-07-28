---
name: gerar-destaques-curtos
description: Produz o texto enxuto de destaques (3 a 5 marcadores, frases secas) no tom objetivo esperado pelo operador, para acompanhar a entrega do relatório (uso interno, ao operador). Usado pelo Validador após aprovar.
allowed-tools: Read
---

# gerar-destaques-curtos

## Especificação
- **Muito curto**: 3 a 5 marcadores, frases secas. Eduardo prefere comunicação curta e objetiva. Nada de parágrafos.
- Conteúdo sugerido: período; volume (conversas/sessões); % sem resposta; % de conversas atendidas; e 1 ponto de atenção factual (se houver).
- Sem juízo de valor, sem recomendação. Apenas os destaques que saltam dos números.

## Formato
```
Semana: {período}
• Volume: {n} conversas atribuídas · {n} sessões no fluxo
• % sem resposta: {x}%
• % de conversas atendidas: {x}%
• {1 ponto de atenção factual, se houver}
```

## Regra
- Os números vêm do pacote/relatório já validado. Não recalcular nem reinterpretar.
