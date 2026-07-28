---
name: parametrizar-script-semanal
description: Zera SEMANA_INICIO/SEMANA_FIM/DATA_REFERENCIA para a execução automática (ou define a semana no reprocessamento) e aponta ARQUIVO para o unificado da semana. Passo 0 CRÍTICO do Cientista, antes de rodar.
allowed-tools: Read, Edit
---

# parametrizar-script-semanal

## Por que é crítico
No topo de `analise_treble_semanal.py`, `SEMANA_INICIO`/`SEMANA_FIM` têm **PRIORIDADE sobre tudo**. Se ficarem preenchidos, o script analisa sempre aquela semana antiga.

## Forma recomendada (execução automática): CLI, sem editar o script
Rodar da **raiz do projeto** passando SÓ o período `DD-MM-AAAA a DD-MM-AAAA`:
```bash
python scripts/geral/analise_treble_semanal.py "12-07-2026 a 18-07-2026"
```
Desde 06/07/2026 o script localiza sozinho o unificado em `analises/[período] (geral)/Dados_Treble_Semana.xlsx`. **Passar um caminho como argumento falha** ("Formato inválido"): o argumento é só o período. Nesta forma não é preciso editar variável nenhuma.

## Forma alternativa (caminho fora do padrão ou reprocessamento): editar variáveis do topo
```python
ARQUIVO = r"analises/DD-MM-AAAA a DD-MM-AAAA (geral)/Dados_Treble_Semana.xlsx"
DATA_REFERENCIA = None
SEMANA_INICIO   = None   # None = detecção automática pela semana anterior
SEMANA_FIM      = None
```
Com os três como `None`, o script detecta a janela pelos próprios dados (e, na ausência, cai na semana anterior a hoje). Para **reprocessar uma semana antiga**, preencher `SEMANA_INICIO`/`SEMANA_FIM` com as datas (dom/sáb) daquela semana e apontar `ARQUIVO` para o unificado correspondente.

## Regra
- Conferir o caminho de `ARQUIVO` (o nome real do unificado é `Dados_Treble_Semana.xlsx`).
- Não editar a lógica do script, apenas as variáveis de configuração.
