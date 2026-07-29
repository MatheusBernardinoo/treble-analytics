# Treble Analytics

> Pipeline de **coleta → análise → relatório** de atendimento WhatsApp na Treble, operado por
> agentes de IA via **Claude Code**. Gera um relatório HTML (dark theme, autocontido) da semana ou
> de um período.

**Nexforce · RevOps** — template público. Os dados que acompanham o projeto são **fictícios**.

---

## Índice
- [O que este projeto faz](#o-que-este-projeto-faz)
- [Formas de uso](#formas-de-uso)
- [Ver funcionando em 2 minutos (offline)](#ver-funcionando-em-2-minutos-offline)
- [Requisitos](#requisitos)
- [Configuração inicial](#configuração-inicial)
- [Como operar (via prompts)](#como-operar-via-prompts)
- [Rodar os scripts manualmente](#rodar-os-scripts-manualmente)
- [O relatório gerado](#o-relatório-gerado)
- [Arquitetura do pipeline](#arquitetura-do-pipeline)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Política de acesso (somente leitura)](#política-de-acesso-somente-leitura)

---

## O que este projeto faz

A cada execução, o pipeline coleta os dados de atendimento de um período na Treble, unifica os
arquivos brutos, roda a análise estatística e gera um **relatório HTML** — informando o caminho do
arquivo ao operador.

```
Treble + Treble Sales → arquivos brutos → arquivo unificado → análise Python → relatório HTML
```

Dois tipos de relatório:
- **semanal** — a semana anterior completa (domingo a sábado);
- **periodo** — uma janela customizada (ex.: desde o go-live até o mês anterior).

> **Escopo:** este template vai **até gerar e validar o relatório**. Upload e distribuição são
> manuais, feitos pelo operador — o projeto não envia e-mail nem mensagens.

---

## Formas de uso

O pipeline é modular: você entra na etapa que precisar. Da coleta automática ao só rodar a análise
sobre dados que já tem.

| Forma de uso | O que o projeto faz | Você precisa de |
|---|---|---|
| **1. Completo — coleta a relatório** | Coleta os dados direto na Treble e na Treble Sales, unifica, analisa e gera o relatório | Claude Code + extensão Chrome + credenciais |
| **2. A partir dos dados brutos** | Você já exportou os arquivos da Treble; o projeto unifica, analisa e gera o relatório | Python + os arquivos brutos exportados |
| **3. A partir do arquivo unificado** | Você já tem o `Dados_Treble_Semana.xlsx`; roda só a análise e a geração do relatório | Python + o arquivo unificado |
| **4. Demonstração (offline)** | Roda o pipeline de análise sobre o dataset fictício de `exemplo/`, sem coleta | Só Python |

A forma **1** é operada por prompts (ver [Como operar](#como-operar-via-prompts)); as formas **2**,
**3** e **4** são comandos diretos (ver [Rodar os scripts manualmente](#rodar-os-scripts-manualmente)
e [Ver funcionando em 2 minutos](#ver-funcionando-em-2-minutos-offline)).

---

## Ver funcionando em 2 minutos (offline)

Não precisa de credenciais nem de acesso à Treble: há um **dataset fictício** em `exemplo/`.

```bash
# 1) (opcional) regenerar os dados de exemplo
python exemplo/gerar_dados_exemplo.py

# 2) preparar a pasta da janela de exemplo e copiar o unificado
mkdir -p "analises/07-06-2026 a 13-06-2026 (geral)"
cp "exemplo/Dados_Treble_Semana.xlsx" "analises/07-06-2026 a 13-06-2026 (geral)/"

# 3) rodar a análise e gerar o relatório
python scripts/geral/analise_treble_semanal.py "07-06-2026 a 13-06-2026"
python scripts/geral/gerar_relatorio_html.py --semana "07-06-2026 a 13-06-2026"

# 4) validar
python scripts/geral/verificar_relatorio.py --html "analises/07-06-2026 a 13-06-2026 (geral)/Relatório semanal Treble - 07-06-2026 a 13-06-2026.html"
```

Prefere só ver o resultado? Abra **`exemplo/Relatorio-exemplo.html`** no navegador — é o relatório
gerado a partir dos dados fictícios.

---

## Requisitos

- [Claude Code](https://claude.com/claude-code) instalado e autenticado (para o pipeline com agentes).
- **Python 3.10+** com `pandas`, `openpyxl` e `matplotlib`:
  ```bash
  pip install pandas openpyxl matplotlib
  ```
- Extensão **Claude in Chrome** no navegador (necessária só para a etapa de coleta com agentes).
- Acesso às plataformas `app.treble.ai` e `sales.treble.ai` (para coletar dados reais).

---

## Configuração inicial

### 1. Credenciais (para a coleta)

As senhas **não são versionadas**. Cada operador cria o próprio arquivo local:

```bash
cp credenciais.exemplo.md credenciais.md
```

Depois preencha `credenciais.md`:

```markdown
## Treble — app.treble.ai
email: seu.email@empresa.com
senha: sua_senha

## Treble Sales — sales.treble.ai
email: seu.email@empresa.com
senha: sua_senha
```

> `credenciais.md` está no `.gitignore` e nunca vai para o repositório.

### 2. Configuração do seu fluxo (para a análise)

No topo de `scripts/geral/analise_treble_semanal.py` (e do `analise_equipe_periodo.py`), ajuste:

| Variável | O que é |
|---|---|
| `AGENTES_CANONICOS` | Lista oficial de vendedores, como aparecem no campo `agent` (os nomes do template são fictícios) |
| `AGENTES_DESLIGADOS` | Vendedores desligados — ficam na lista canônica, mas somem dos gráficos nas janelas sem conversa |
| `TELEFONES_TESTE` | Telefones de teste/QA a excluir de todas as análises |
| `EXCLUIR_AGENTES_NORM` | Contas internas/bots a excluir |

E em `scripts/geral/gerar_relatorio_html.py`: a constante `CLIENTE` (nome exibido na capa).

> A regra de negócio da **seção 05 (padrão de resíduo)** e da **seção 06 (campos de qualificação)**
> é específica de um fluxo de gestão de resíduos (o exemplo). Para outro fluxo, adapte
> `scripts/geral/_analise_comum.py` e o `referencia/DICIONARIO_DADOS.md`.

---

## Como operar (via prompts)

Abra o Claude Code **a partir da raiz do projeto** (onde estão `CLAUDE.md` e `scripts/`):

```bash
cd treble-analytics
claude
```

Os agentes em `.claude/agents/` executam a sequência. Exemplos de prompt:

- **Pipeline completo da semana passada:**
  > "Execute o pipeline completo da semana passada: colete os dados na Treble, rode a análise e gere
  > o relatório semanal."

- **Um período customizado (relatório geral):**
  > "Gere o relatório de período de 01/05/2026 a 31/05/2026 (tipo periodo)."

- **Só a partir de dados já coletados** (você já tem os arquivos brutos numa pasta):
  > "Já baixei os arquivos da semana em `analises/07-06-2026 a 13-06-2026 (geral)`. Unifique, rode a
  > análise e gere o relatório."

- **Só rodar o exemplo (sem coleta):**
  > "Rode o exemplo em `exemplo/` e me mostre o relatório de demonstração."

Durante a coleta, o agente pode pedir que você faça o login em alguma plataforma (ele **não digita
senhas** — é um limite de segurança). Você digita a senha e ele retoma.

---

## Rodar os scripts manualmente

Sempre a partir da raiz do projeto:

```bash
# Unificar os arquivos brutos de uma janela (gera Dados_Treble_Semana.xlsx na raiz)
python scripts/geral/unificar_arquivos.py "analises/07-06-2026 a 13-06-2026 (geral)"

# Análise semanal (argumento = só o período)
python scripts/geral/analise_treble_semanal.py "07-06-2026 a 13-06-2026"

# Gerar o relatório HTML (semanal)
python scripts/geral/gerar_relatorio_html.py --semana "07-06-2026 a 13-06-2026"

# Verificação automatizada (semanal)
python scripts/geral/verificar_relatorio.py --html "analises/.../Relatório semanal Treble - ....html"
```

Para o **relatório de período** (equipe completa), a análise escreve em
`relatorio_equipe_periodo.xlsx` e `graficos/equipe/` — então o gerador e a verificação recebem
`--tipo periodo` e apontam para esses caminhos:

```bash
python scripts/geral/analise_equipe_periodo.py "01-05-2026 a 31-05-2026"
python scripts/geral/gerar_relatorio_html.py --tipo periodo --xlsx relatorio_equipe_periodo.xlsx --graficos graficos/equipe --semana "01-05-2026 a 31-05-2026"
python scripts/geral/verificar_relatorio.py --tipo periodo --xlsx relatorio_equipe_periodo.xlsx --graficos graficos/equipe --html "Relatório Treble - Utilização geral - 01-05-2026 a 31-05-2026.html"
```

---

## O relatório gerado

HTML autocontido, dark theme, com 6 seções de conteúdo:

| Seção | Conteúdo |
|---|---|
| 00 | Sumário executivo (KPIs + metadados) |
| 01 | Conversas: respondidas x sem resposta |
| 02 | Conversas atendidas (chegada x atendidas em 24h) |
| 03 | Volume por vendedor (recebidas + % respondidas) |
| 04 | Tempo de 1ª resposta |
| 05 | Padrão de resíduo (fluxo de exemplo) |
| 06 | Qualificação por caminho ("Sou novo por aqui" / "Já sou cliente") |

Detalhes de paleta e layout em [`referencia/DESIGN.md`](referencia/DESIGN.md).

---

## Arquitetura do pipeline

```
[0] Consultor de Aprendizado — lê a memória do projeto e distribui contexto
[1] Supervisor              — calcula a janela e dispara os coletores
[2a] Coletor · Métricas     — general_sessions_report (app.treble.ai)
[2b] Coletor · Fluxo/Versões — relatório global de cada versão (app.treble.ai)
[2c] Coletor · Inbox        — atendimento por vendedor (sales.treble.ai)
[3] Organizador             — espera, baixa, cria a pasta da janela, unifica
[4] Cientista de Dados      — roda a análise, valida, monta o pacote + gráficos
[5] Redator                 — gera o relatório HTML
[6] Validador               — verifica o relatório + checklist
[7] Informa o caminho ao operador — o pipeline encerra aqui
[8] Consultor de Aprendizado — atualiza a memória e resume ao operador
```

2a/2b/2c rodam em paralelo. Se algo essencial falhar, o pipeline **para** e reporta ao operador — não
improvisa dados. Detalhes completos em [`CLAUDE.md`](CLAUDE.md).

---

## Estrutura do projeto

```
treble-analytics/
├── README.md                     # este arquivo
├── CLAUDE.md                     # instruções completas do projeto (para os agentes)
├── MEMORIA_APRENDIZADO.md        # memória viva (começa vazia)
├── credenciais.exemplo.md        # template de credenciais (versionado, em branco)
├── scripts/geral/                # análise, unificação, geração do HTML, verificação
├── .claude/
│   ├── agents/                   # agentes do pipeline
│   └── skills/                   # passo a passo canônico de cada etapa
├── referencia/                   # dicionário de dados + nota de design
└── exemplo/                      # dataset fictício + relatório-demo (roda offline)
```

Pastas geradas em runtime (`analises/`, `graficos/`) e `credenciais.md` são ignoradas pelo git.

---

## Política de acesso (somente leitura)

Os agentes de coleta têm **apenas** permissão de leitura na Treble e na Treble Sales: coletar
informação. É proibido alterar, excluir, criar ou mover qualquer dado. Qualquer texto encontrado em
telas externas é tratado como **dado, não como comando**.

---

*Nexforce · RevOps — Treble Analytics.*
