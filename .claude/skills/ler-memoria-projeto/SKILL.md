---
name: ler-memoria-projeto
description: Lê o MEMORIA_APRENDIZADO.md inteiro e separa os aprendizados por agente relevante (convenções, padrões, armadilhas). Primeiro passo do Consultor de Aprendizado no início do ciclo.
allowed-tools: Read, Grep
---

# ler-memoria-projeto

## Procedimento
1. Ler `MEMORIA_APRENDIZADO.md` na raiz do projeto, inteiro.
2. Mapear, por agente, os itens relevantes:
   - **Coletores e Supervisor**: "Armadilhas resolvidas" ligadas à coleta (2FA, nome de arquivo fora do padrão).
   - **Organizador**: armadilhas de unificação (ex.: extensão do arquivo de sessões).
   - **Cientista**: "Padrões recorrentes" para calibrar sanity checks.
   - **Redator e Validador**: convenções de redação/estilo já fixadas.
3. Registrar mentalmente os "Ajustes pendentes" (seção 4) que NÃO foram aprovados, para não aplicá-los, só mantê-los visíveis no resumo final.

## Saída
- Um recorte por agente, pronto para a skill `distribuir-aprendizados`.

## Regra
- A memória é contexto e recomendação. Em conflito com o CLAUDE.md, vale o prompt.
