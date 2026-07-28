---
name: paleta-graficos
description: Define a paleta de cores e regras de nomenclatura para todos os gráficos do relatório Treble. Usada pelo Cientista de Dados ao gerar PNGs via matplotlib. Garante consistência visual entre relatórios semanais e de período.
allowed-tools: []
---

# paleta-graficos: cores e nomenclatura dos gráficos

## Paleta oficial

| Constante     | Hex       | Uso                                                        |
|---------------|-----------|------------------------------------------------------------|
| `COR_OK`      | `#2E8B57` | Verde — métrica positiva (conversas atendidas, respondidas) |
| `COR_ALERTA`  | `#C0392B` | Vermelho — métrica negativa (não respondidas, não atendidas) |
| `COR_AMBAR`   | `#E08E0B` | Âmbar — métrica neutra (tempo de resposta, volume geral)   |
| `COR_AZUL`    | `#1F5C99` | Azul — série principal / destaque neutro                   |
| `COR_CIANO`   | `#5FA8DC` | Ciano — volume total chegado (chegaram ao vendedor)        |
| `COR_CINZA`   | `#AAB4BF` | Cinza — categoria IA ou dado residual                      |
| `COR_NAVY`    | `#0F2A47` | Azul escuro — títulos dos gráficos e anotações             |

## Regra de ouro — psicologia da cor

**Verde = bom. Vermelho = ruim. Nunca o inverso.**

- "Conversas atendidas" → `COR_OK` (verde)
- "Conversas não atendidas" → `COR_ALERTA` (vermelho)
- "Conversas respondidas" → `COR_OK` (verde)
- "Sem resposta" / "não respondidas" → `COR_ALERTA` (vermelho)
- Tempo de resposta (valor neutro, nem bom nem ruim por si só) → `COR_AMBAR`
- Volume total / chegadas → `COR_CIANO`

Se a mesma métrica aparecer em dois gráficos diferentes, usa a mesma cor nos dois. Consistência não é opcional.

## Nomenclatura padronizada (regra única, sem variação)

O termo canônico para conversas com primeira resposta em até 24h (janela da Meta) é **"conversas atendidas"**. Nunca variar. A definição (o critério das 24h) aparece UMA vez, na descrição da seção 02 do relatório, não nos rótulos.

| Termo correto               | Proibido (qualquer variação)                        |
|-----------------------------|-----------------------------------------------------|
| Conversas atendidas         | Atendidos em 24h, respondidos em 24h, atendimento em 24h |
| Conversas não atendidas     | Chegaram não atendidos em 24h, não respondidos em 24h |
| Conversas respondidas       | Chats respondidos                                   |
| Conversas recebidas         | Chats recebidos                                     |

Usar "conversas" (não "chats") em todos os títulos de gráficos, rótulos de legenda e leituras. (O relatório HTML não tem captions acima dos gráficos desde o padrão aprovado em 03/07/2026; o título dentro do PNG é o único título do gráfico.)

## Gráficos da S.02 — cadência por tipo de relatório (06/07/2026)

- **Relatório SEMANAL: cadência DIÁRIA, segunda a sexta** (`B_24h_dia.png` + `B_24h_dia_stacked.png`). O fluxo não recebe novos leads no fim de semana; sábado/domingo só entram no eixo se tiverem chegadas (> 0), para nunca esconder dado.
- **Relatório de PERÍODO: cadência SEMANAL** (`B_24h.png` + `B_24h_stacked.png`).
- As regras visuais abaixo valem para as duas cadências.

## Gráfico absoluto da S.02 (B_24h / B_24h_dia) — regras específicas

- Tipo: barras verticais **sobrepostas** (não lado a lado): a barra verde (conversas atendidas) fica DENTRO da barra azul-ciano (chegaram ao vendedor) — mesma posição x, largura menor (ex.: azul 0.62, verde 0.34).
- Motivo: atendidas ⊆ chegaram. Barras lado a lado dão a impressão errada de que os valores se somam.
- Valores absolutos com rótulo em cima de cada barra. Manter absoluto; a proporção é papel do gráfico empilhado.

## Gráfico empilhado da S.02 (B_24h_stacked / B_24h_dia_stacked) — regras específicas

- Tipo: barras verticais empilhadas **100% normalizadas**
- Denominador: `chegaram` (total de chegadas ao vendedor naquela semana/dia)
- `atendidas ⊆ chegaram` — portanto `nao_atendidas = chegaram - atendidas`
- Segmento inferior (verde, `COR_OK`): "Conversas atendidas" — `atendidas / chegaram * 100`
- Segmento superior (vermelho, `COR_ALERTA`): "Conversas não atendidas" — `nao_atendidas / chegaram * 100`
- Cada barra soma **100%** — nunca mostrar total absoluto no topo
- Exibir % dentro de cada segmento quando o segmento for ≥ 8%

## Gráfico D3_tempo_semanal — regras específicas (só relatório de período)

- Tipo: **linha única do TIME** — a análise não é segmentada por vendedor (decisão de 03/07/2026)
- Mediana calculada sobre todas as respostas da semana (não é média das medianas por vendedor)
- Cor: `COR_AMBAR` (tempo é métrica neutra); marcador em cada semana com o valor rotulado acima do ponto
- Eixo y em **horas** (padrão aprovado). O script também gera a variante `D3_tempo_semanal_min.png` em minutos, mas o relatório usa horas salvo pedido explícito (`--d3-unidade min`)

## Gráfico R2_residuo_resp — regras específicas

- Tipo: barras horizontais empilhadas (valores absolutos)
- Segmento esquerdo (verde, `COR_OK`): "respondidos"
- Segmento direito (vermelho, `COR_ALERTA`): "sem resposta"
- Exibir % dentro de cada segmento quando o segmento for ≥ 8%
  - Fórmula: `respondidos / contatos * 100` e `sem_resposta / contatos * 100`
