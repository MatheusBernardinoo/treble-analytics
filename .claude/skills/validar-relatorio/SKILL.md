---
name: validar-relatorio
description: Valida o relatório Treble antes da entrega. Roda verificar_relatorio.py para checks automáticos (xlsx, 10 PNGs, totais, período, HTML), depois aplica checklist de qualidade manual específico para o tipo (semanal ou periodo). Emite veredicto APROVADO / AJUSTAR / REJEITAR. Usado pelo Validador.
allowed-tools: Bash, Read, Glob
---

# validar-relatorio

## Dois tipos de relatório

| Tipo | Entrega | Período | Script de análise | HTML gerado |
|---|---|---|---|---|
| `semanal` | Toda segunda-feira | Dom a sáb anteriores (7 dias) | `analise_treble_semanal.py` | `Relatório semanal Treble - DD-MM-AAAA a DD-MM-AAAA.html` |
| `periodo` | Primeira segunda do mês | Desde o go-live até o mês atual | `analise_equipe_periodo.py` | `Relatório Treble - Utilização geral - DD-MM-AAAA a DD-MM-AAAA.html` |

Ambos usam o mesmo layout (6 seções, 10 gráficos) produzido por `gerar_relatorio_html.py`.

---

## Passo 1 — Identificar o tipo e localizar os artefatos

Determinar o tipo (`semanal` ou `periodo`) a partir do contexto ou do nome do arquivo HTML.

Localizar o HTML e confirmar o caminho:
```powershell
Get-ChildItem -Recurse -Filter "Relat*.html" | Select-Object FullName, Length
```

---

## Passo 2 — Verificação automatizada

Rodar `verificar_relatorio.py` com o tipo correto. **Sempre da raiz do projeto.**

**Para relatório semanal (padrão):**
```bash
python scripts/geral/verificar_relatorio.py
```

**Para relatório semanal com HTML já gerado:**
```bash
python scripts/geral/verificar_relatorio.py --html "Relatório semanal Treble - DD-MM-AAAA a DD-MM-AAAA.html"
```

**Para relatório de período:**
```bash
python scripts/geral/verificar_relatorio.py --tipo periodo --html "Relatório Treble - Utilização geral - DD-MM-AAAA a DD-MM-AAAA.html"
```

O script verifica:
- xlsx existe e está legível
- 10 abas obrigatórias presentes (inclui B_24h_semanal)
- Total de conversas > 0
- Respondidas + Sem resposta = Total (tolerância ±1)
- % sem resposta no intervalo 0–100
- Vendedores com dados em D1_por_vendedor
- Período detectado no xlsx
- Duração coerente com o tipo (7 dias para semanal; 28+ dias para periodo)
- PNGs existem e têm tamanho > 0 (semanal: 10, com B_24h_dia_stacked.png; período: 11, com B_24h_stacked.png e D3_tempo_semanal.png)
- HTML existe com tamanho razoável (> 50 KB)
- Nome do HTML contém período DD-MM-AAAA a DD-MM-AAAA

**Se houver FALHA: parar. Reportar ao Redator (problema de script) ou ao Cientista (problema de dado). Não prosseguir para o checklist manual.**

---

## Passo 3 — Checklist de qualidade manual

Executar APENAS se o Passo 2 passou sem falhas (0 FALHA no relatório do script).

### Checklist comum (semanal e periodo)

- [ ] **Período correto**: o período no relatório bate com o que foi solicitado?
- [ ] **6 seções presentes**: 01 Conversas, 02 Conversas Atendidas, 03 Volume por Vendedor, 04 Tempo de Resposta, 05 Padrão de Resíduo, 06 Qualificação
- [ ] **Seções com 2 gráficos**: seções 02, 03, 05 e 06 têm exatamente 2 gráficos cada (S.03 = D1_recebidos + D2_resp)
- [ ] **Sem redundância**: sumário executivo contém só totais de volume; indicadores detalhados ficam nas seções sem repetição
- [ ] **Sem meta ou objetivo**: nenhum uso de "meta", "objetivo", "ideal", "esperado" ou juízo de valor
- [ ] **Sem sugestões (regra absoluta)**: nenhuma frase sugere ação ou mudança de processo; só dados e relações sutis
- [ ] **Nomenclatura padronizada**: "conversas atendidas" e "conversas respondidas" — sem "atendidos em 24h", "atendimento em 24h" ou "chats" em qualquer variação
- [ ] **Leituras cruzadas**: em seção com 2+ gráficos, a `Leitura:` relaciona dados dos dois gráficos (não resume cada um isoladamente). Exceção de formato: a seção 06 tem UMA Leitura por gráfico; o cruzamento entre os fluxos fica na segunda (após "Já sou cliente"). Nenhuma seção tem bloco "Iniciativa" (exceção única: o relatório de referência)
- [ ] **Top 3 correto**: linha "Maior % de resposta — vendedores" traz os 3 maiores percentuais de resposta, não os maiores volumes
- [ ] **Tom factual**: blocos `Leitura:` descrevem o que o número é, nunca o que deveria ser
- [ ] **Sem fora de escopo**: nada de SLA 72h, AUTO×MANUAL, última mensagem, transferências por vendedor, destino de sessões
- [ ] **Alertas refletidos**: se o pacote tinha alertas de dados parciais, o relatório menciona isso
- [ ] **Leitura coerente**: textos narrativos são consistentes com os gráficos ao lado
- [ ] **Sem captions**: nenhum título cinza (`class="caption"`) acima dos gráficos — padrão aprovado em 03/07/2026; a descrição da seção é o único texto antes do primeiro gráfico
- [ ] **Sem Iniciativa**: nenhum bloco `Iniciativa:` (exceção única e já entregue: o relatório de referência)
- [ ] **Sem informação equivalente repetida (regra absoluta 06/07/2026)**: sem "% de atendimento realizado" (equivale a "% de conversas atendidas"); tabela de resíduo sem coluna "% sem resposta" (complemento de "% respondida")
- [ ] **Sem explicar o processo do cliente ao cliente (regra absoluta 10/07/2026)**: nenhuma frase descrevendo o funcionamento do fluxo/operação do cliente (ex.: "não recebe novos leads no fim de semana", "coleta N campos")
- [ ] **Vendedores desligados fora dos gráficos**: desligado sem recebidas na janela não aparece nos gráficos por vendedor
- [ ] **S.02 na cadência certa**: semanal = diária seg–sex (B_24h_dia*); período = semanal (B_24h*)
- [ ] **Gráficos de % por vendedor** sem ninguém com 0 conversas recebidas
- [ ] **Desempate claro e sutil**: empates em ranking (maior/menor %) explicam o porquê na Leitura de forma natural ("por ter o maior volume entre os vendedores com X% de resposta"), sem anunciar "critério de desempate"
- [ ] **Gráficos da S.06 na ordem real do fluxo** (1ª pergunta no topo), casando com a narrativa de quedas da Leitura

### Checklist adicional — tipo `semanal`

- [ ] Período = dom a sáb da semana ANTERIOR (não a semana corrente)
- [ ] Título da capa contém "Semanal" ou equivalente
- [ ] Seção 02 mostra cadência DIÁRIA seg–sex (`B_24h_dia*`), não por semana

### Checklist adicional — tipo `periodo`

- [ ] Período inicia na data de go-live (ou data acordada) e vai até o fim do mês anterior
- [ ] Volume de conversas condizente com o acumulado (esperar 100+ para 2+ meses)
- [ ] Seção 02 (Conversas Atendidas) mostra distribuição ao longo de semanas/meses
- [ ] Seção 03 (Volume por Vendedor) reflete acumulado do período completo, com distribuição por vendedor
- [ ] Seção 04 tem o gráfico de evolução semanal como LINHA ÚNICA do time, eixo em horas (sem segmentação por vendedor)

**Referência visual canônica (ambos os tipos):** `o formato de referência do projeto` — versão aprovada pelo operador em 03/07/2026. Desvios de formato em relação a ela são motivo de AJUSTAR (exceto o bloco `Iniciativa:`, exclusivo dela).

---

## Passo 4 — Veredicto

### APROVADO
```
Verificação automatizada: N checks, 0 falhas.
Checklist manual: todos os itens concluídos.
APROVADO — pronto para entrega.

Período: DD-MM-AAAA a DD-MM-AAAA | Tipo: semanal|periodo
Total: N conversas | % sem resposta: X% | % de conversas atendidas: X%
```

### AJUSTAR (problema de redação — devolver ao Redator)
```
AJUSTAR — devolver ao Redator.
Problema: [item específico do checklist manual que falhou]
O Redator tem uma rodada de ajuste.
```

### REJEITAR (problema de dado — escalar ao Cientista)
```
REJEITAR — escalar ao Cientista.
Problema: [falha específica do verificar_relatorio.py ou inconsistência detectada]
O dado está incorreto na origem; o Redator não pode corrigir isso.
```

---

## Regra

Um número errado custa mais que um atraso. Em dúvida sobre integridade do dado, parar e sinalizar. Nunca aprovar com FALHA no verificador automatizado.
