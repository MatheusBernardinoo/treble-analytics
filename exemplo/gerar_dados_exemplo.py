# -*- coding: utf-8 -*-
"""
gerar_dados_exemplo.py
Gera um arquivo unificado FICTÍCIO (Dados_Treble_Semana.xlsx) para rodar o
pipeline de análise SEM credenciais nem dados reais. Serve também como
documentação do schema: mostra as abas e colunas que os scripts esperam.

Uso:
    python exemplo/gerar_dados_exemplo.py
Gera: exemplo/Dados_Treble_Semana.xlsx  (abas: atendimento-treble, sessoes-gerais, Versao 1)

Depois, para ver o relatório de demonstração (a partir da raiz do projeto):
    # copie o arquivo para a pasta da janela de exemplo
    mkdir -p "analises/07-06-2026 a 13-06-2026 (geral)"
    cp "exemplo/Dados_Treble_Semana.xlsx" "analises/07-06-2026 a 13-06-2026 (geral)/"
    python scripts/geral/analise_treble_semanal.py "07-06-2026 a 13-06-2026"
    python scripts/geral/gerar_relatorio_html.py --semana "07-06-2026 a 13-06-2026"
"""
import os
import random
from datetime import datetime, timedelta

import pandas as pd

random.seed(42)

# Deve casar com AGENTES_CANONICOS dos scripts de análise (nomes fictícios).
AGENTES = [
    "Ana Souza", "Bruno Costa", "Carla Mendes", "Daniel Rocha",
    "Eduarda Nunes", "Felipe Ramos", "Beatriz Dias", "Henrique Alves",
    "Isabela Pinto", "Larissa Gomes", "Marcos Vieira", "Renata Oliveira",
]

# Janela de exemplo (domingo a sábado)
INICIO = datetime(2026, 6, 7)   # domingo
DIAS_UTEIS = [INICIO + timedelta(days=d) for d in range(1, 6)]  # seg..sex

def telefone(i):
    return f"+5511900{i:06d}"

def ts(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# Pool de telefones (contatos). Os primeiros são compartilhados entre as abas.
N_CONTATOS = 70
telefones = [telefone(i) for i in range(N_CONTATOS)]

# --------------------------------------------------------------------------
# ABA atendimento-treble (base de verdade — uma linha por conversa com vendedor)
# --------------------------------------------------------------------------
atend = []
N_ATEND = 45
for i in range(N_ATEND):
    tel = telefones[i]                       # 45 primeiros telefones têm atendimento
    agente = random.choice(AGENTES)
    dia = random.choice(DIAS_UTEIS)
    assigned = dia + timedelta(hours=random.randint(8, 18), minutes=random.randint(0, 59))
    respondeu = random.random() < 0.35       # ~35% respondidas
    if respondeu:
        first = assigned + timedelta(hours=round(random.uniform(0.1, 22), 2))
        finish = random.choice(["MANUAL", "MANUAL", "AUTO"])
        sender = random.choice(["AGENT", "USER"])
    else:
        first = None
        finish = "AUTO"
        sender = random.choice(["USER", "IA"])
    # poucas transferências
    if random.random() < 0.12:
        ltf = f"{random.choice(AGENTES).split()[0].lower()}@empresa.com"
        ltt = ts(assigned + timedelta(minutes=random.randint(5, 120)))
    else:
        ltf, ltt = "", ""
    atend.append({
        "phone": tel,
        "agent": agente,
        "created_at": ts(assigned - timedelta(minutes=random.randint(1, 90))),
        "assigned_at": ts(assigned),
        "agent_first_message": ts(first) if first else "",
        "finish_type": finish,
        "last_message_sender": sender,
        "last_transfer_from": ltf,
        "last_transfer_time": ltt,
    })
df_atend = pd.DataFrame(atend)

# --------------------------------------------------------------------------
# ABA sessoes-gerais (log de sessões do fluxo)
# --------------------------------------------------------------------------
sess = []
N_SESS = 220
status_opts = ["HumanHandover", "Completed", "Expired", "InProgress"]
for i in range(N_SESS):
    tel = random.choice(telefones)
    dia = random.choice(DIAS_UTEIS + [INICIO, INICIO + timedelta(days=6)])  # inclui fds
    started = dia + timedelta(hours=random.randint(7, 20), minutes=random.randint(0, 59))
    finished = started + timedelta(minutes=random.randint(1, 240))
    sess.append({
        "user_cellphone": tel,
        "session_started_timestamp": ts(started),
        "first_message_timestamp": ts(started + timedelta(seconds=random.randint(1, 60))),
        "last_message_timestamp": ts(finished),
        "session_finished_timestamp": ts(finished),
        "session_status": random.choice(status_opts),
        "conversation_version": "1",
        "last_message": random.choice(["ok", "obrigado", "quero saber mais", ""]),
        "last_node_id": f"node_{random.randint(1, 40)}",
    })
df_sess = pd.DataFrame(sess)

# --------------------------------------------------------------------------
# ABA Versao 1 (qualificação do fluxo — variáveis HubSpot)
# --------------------------------------------------------------------------
CAMINHO_COL = "você é novo por aqui ou já é cliente?"
TIPOS = ["Industrial", "Hospitalar"]
CLASSES = ["Perigoso (Classe 1)", "Não perigoso (Classe 2)", "Não sei informar", ""]
SERVICOS = ["Coleta", "Transporte", "Destinação", ""]

def maybe(valor, prob):
    """Retorna valor com probabilidade prob, senão string vazia (campo não preenchido)."""
    return valor if random.random() < prob else ""

ver = []
# todos os telefones do atendimento aparecem aqui (para a S.05 ter dados) + extras
tel_versao = telefones[:]  # 70
for idx, tel in enumerate(tel_versao):
    r = random.random()
    if r < 0.45:
        caminho = "Sou novo por aqui"
    elif r < 0.60:
        caminho = "Já sou cliente"
    else:
        caminho = ""  # não escolheu caminho
    novo = caminho == "Sou novo por aqui"
    cli = caminho == "Já sou cliente"
    # completude decrescente ao longo do fluxo (mais alta no começo)
    ver.append({
        "Celular": tel,
        CAMINHO_COL: caminho,
        "hubspot_email": maybe(f"contato{idx}@exemplo.com", 0.86 if novo else (0.6 if cli else 0.2)),
        "hubspot_firstname": maybe(f"Contato {idx}", 0.83 if novo else (0.58 if cli else 0.18)),
        "hubspot_company": maybe(f"Empresa {idx}", 0.68 if novo else 0.0),
        "hubspot_cpf": maybe(f"000.000.{idx:03d}-00", 0.30 if novo else (0.25 if cli else 0.0)),
        "hubspot_cnpj": maybe(f"00.000.{idx:03d}/0001-00", 0.25 if novo else (0.22 if cli else 0.0)),
        "hubspot_state": maybe("SP", 0.51 if novo else 0.0),
        "hubspot_city": maybe("São Paulo", 0.48 if novo else 0.0),
        "hubspot_tipo_de_residuo": maybe(random.choice(TIPOS), 0.40 if novo else (0.33 if cli else 0.1)),
        "hubspot_truora_classe_residuo": maybe(random.choice(CLASSES), 0.36 if novo else 0.30),
        "hubspot_truora_quantidade_residuo": maybe(f"{random.randint(1, 50)} kg", 0.32 if novo else (0.28 if cli else 0.0)),
        "hubspot_truora_tipo_de_servico": maybe(random.choice(SERVICOS), 0.29 if novo else (0.22 if cli else 0.0)),
    })
df_ver = pd.DataFrame(ver)

# --------------------------------------------------------------------------
# Grava o arquivo unificado
# --------------------------------------------------------------------------
OUT = os.path.join(os.path.dirname(__file__), "Dados_Treble_Semana.xlsx")
with pd.ExcelWriter(OUT, engine="openpyxl") as w:
    df_atend.to_excel(w, sheet_name="atendimento-treble", index=False)
    df_sess.to_excel(w, sheet_name="sessoes-gerais", index=False)
    df_ver.to_excel(w, sheet_name="Versao 1", index=False)

print(f"[ok] {OUT}")
print(f"     atendimento-treble: {len(df_atend)} linhas | sessoes-gerais: {len(df_sess)} | Versao 1: {len(df_ver)}")
