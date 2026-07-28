---
name: calcular-janela-semana
description: Deriva o domingo e o sábado da semana ANTERIOR a partir da data de execução (a segunda-feira) e entrega o par de datas em formato padronizado. Primeiro passo do Supervisor; o mesmo período é distribuído aos três coletores.
allowed-tools: Bash, Read
---

# calcular-janela-semana

## Regra
- Primeiro dia = **domingo** da semana anterior.
- Último dia = **sábado** da semana anterior.
- Ex.: rodando na segunda 15/06/2026 → janela **07/06/2026 (dom) a 13/06/2026 (sáb)**.

## Procedimento
Calcular a partir de hoje (ou da `DATA_REFERENCIA`, se for reprocessamento). Comando de apoio (Git Bash):
```bash
# domingo anterior e sábado anterior, formato DD-MM-AAAA
python -c "import datetime as d; t=d.date.today(); dom=t-d.timedelta(days=t.weekday()+8); sab=dom+d.timedelta(days=6); print(dom.strftime('%d-%m-%Y'),'a',sab.strftime('%d-%m-%Y'))"
```
(Em Python, `weekday()` 0=segunda. Para segunda a sábado, `t.weekday()+8` recua ao domingo da semana anterior. Para execução manual em **domingo**: passar `DATA_REFERENCIA` = a segunda-feira desejada para evitar recuar duas semanas.)

## Saída
- Par de datas padronizado: `DD-MM-AAAA a DD-MM-AAAA` (para a pasta da semana) e as datas dom/sáb para os coletores selecionarem no calendário.

## Regra de distribuição
- Calcular UMA vez e entregar o MESMO período aos três coletores, para que todos usem exatamente a mesma janela.
