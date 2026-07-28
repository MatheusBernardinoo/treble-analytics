---
name: espera-processamento-treble
description: Executa o padrão de 4x sleep 30 (2 min) para aguardar a Treble gerar os relatórios sem estourar o limite de ~45s por comando do sandbox. Primeiro passo do Organizador.
allowed-tools: Bash
---

# espera-processamento-treble

## Por quê
A Treble leva um tempo para gerar os relatórios; é preciso esperar antes de tentar baixá-los. O ambiente encerra comandos que passam de ~45 segundos, então encadeamos quatro `sleep 30` em vez de um `sleep 120`.

## Procedimento
Rodar `sleep 30` **quatro vezes seguidas** (total ~2 minutos). Cada chamada é um comando separado, nunca `sleep 120`.
```bash
sleep 30
```
(repetir 4x)

## Regra
- Não substituir por `sleep 120` (estoura o limite). Não pular a espera (os relatórios podem ainda não estar prontos).
