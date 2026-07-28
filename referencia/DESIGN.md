# Design do relatório HTML

O relatório é um **HTML autocontido** (dark theme), gerado por
`scripts/geral/gerar_relatorio_html.py`. Os PNGs dos gráficos são embutidos como base64 — o arquivo
funciona offline, sem dependências externas. O layout é fixo; o que muda é o conteúdo.

## Paleta (dark theme)

| Papel | Cor |
|---|---|
| Fundo | `#000000` |
| Surface (cards de fundo) | `#111111` |
| Azul de destaque (accent) | `#1A6FFF` |
| Texto principal | `#FFFFFF` |
| Texto de corpo | `#C8C5BE` |
| Bordas | `#2A2A2A` |

Fontes: **Lato** (corpo) + **JetBrains Mono** (labels/monospace). Gráficos ficam em cards claros;
os blocos `Leitura:` têm fundo azul-claro com borda lateral azul.

## Cores dos gráficos (semântica)

Definidas na skill `.claude/skills/paleta-graficos`:

- **Verde** = bom (ex.: "conversas atendidas").
- **Vermelho** = ruim (ex.: "não atendidas / sem resposta").
- **Âmbar** = neutro (ex.: tempo de resposta).

No gráfico de chegada x atendidas (absoluto), a barra verde (atendidas) fica **dentro** da azul
(chegaram) — mesma posição x, largura menor — para deixar claro que atendidas ⊆ chegaram.

## Estrutura (capa + 6 seções)

Capa com KPIs + tabela de metadados, e as seções 01–06 (ver `CLAUDE.md` → "Estrutura do
relatório"). Sem títulos cinza (captions) acima dos gráficos: a descrição da seção é o único texto
antes do primeiro gráfico.

## Flags úteis do gerador

- `--tipo semanal|periodo` — cadência da seção 02 (diária seg–sex no semanal; semanal no período).
- `--semana "DD-MM-AAAA a DD-MM-AAAA"` — período do relatório.
- `--d3-unidade h|min` — unidade do eixo da evolução de tempo (S.04, só período). Padrão: `h`.
- `--com-titulos` — inclui os captions cinza (só para comparação; o padrão é SEM).

O nome do cliente exibido na capa vem da constante `CLIENTE` no topo do gerador.
