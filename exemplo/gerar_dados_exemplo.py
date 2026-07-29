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

# Pool de telefones (contatos). Os primeiros N_ATEND são compartilhados com o
# atendimento (contatos que chegaram a um vendedor).
N_CONTATOS = 160
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
#
# Modelo de FUNIL: cada contato preenche um PREFIXO dos campos, na ordem do
# fluxo (quem abandona para de preencher os próximos). Com limiares CRESCENTES,
# a taxa de preenchimento cai a cada campo — é a "escadinha" da seção 06.
# Contatos que chegaram a um vendedor (atendidos) vão fundo o bastante para
# informar o tipo de resíduo — assim a seção 05 não tem "Tipo não informado".
# --------------------------------------------------------------------------
CAMINHO_COL = "você é novo por aqui ou já é cliente?"
TIPOS = ["Industrial", "Hospitalar"]
CLASSES = ["Perigoso (Classe 1)", "Não perigoso (Classe 2)", "Não sei informar"]
SERVICOS = ["Coleta", "Transporte", "Destinação"]

# Ordem REAL do fluxo (igual a FLOW_NOVO / FLOW_CLI em _analise_comum.py)
FLOW_NOVO = ["email", "nome", "empresa", "cpf/cnpj", "estado", "cidade",
             "classe_residuo", "tipo_residuo", "qtd_residuo", "tipo_servico"]
FLOW_CLI  = ["email", "nome", "cpf/cnpj", "tipo_residuo", "qtd_residuo", "tipo_servico"]
# limiares crescentes -> preenchimento decrescente (escadinha)
THR_NOVO = [0.03, 0.10, 0.20, 0.32, 0.43, 0.52, 0.59, 0.65, 0.73, 0.81]
THR_CLI  = [0.03, 0.13, 0.28, 0.43, 0.60, 0.74]

COLS_VER = ["Celular", CAMINHO_COL, "hubspot_email", "hubspot_firstname",
            "hubspot_company", "hubspot_cpf", "hubspot_cnpj", "hubspot_state",
            "hubspot_city", "hubspot_truora_classe_residuo",
            "hubspot_tipo_de_residuo", "hubspot_truora_quantidade_residuo",
            "hubspot_truora_tipo_de_servico"]

def preencher_campo(campo, idx, row):
    if campo == "email":            row["hubspot_email"] = f"contato{idx}@exemplo.com"
    elif campo == "nome":           row["hubspot_firstname"] = f"Contato {idx}"
    elif campo == "empresa":        row["hubspot_company"] = f"Empresa {idx}"
    elif campo == "cpf/cnpj":       row["hubspot_cpf"] = f"000.000.{idx:03d}-00"
    elif campo == "estado":         row["hubspot_state"] = "SP"
    elif campo == "cidade":         row["hubspot_city"] = "São Paulo"
    elif campo == "classe_residuo": row["hubspot_truora_classe_residuo"] = random.choice(CLASSES)
    elif campo == "tipo_residuo":   row["hubspot_tipo_de_residuo"] = random.choice(TIPOS)
    elif campo == "qtd_residuo":    row["hubspot_truora_quantidade_residuo"] = f"{random.randint(1, 50)} kg"
    elif campo == "tipo_servico":   row["hubspot_truora_tipo_de_servico"] = random.choice(SERVICOS)

ver = []
for idx, tel in enumerate(telefones):
    atendido = idx < N_ATEND                 # os N_ATEND primeiros chegaram a um vendedor
    r = random.random()
    if atendido:                             # quem foi atendido escolheu um caminho
        caminho = "Sou novo por aqui" if r < 0.70 else "Já sou cliente"
    else:
        caminho = ("Sou novo por aqui" if r < 0.42
                   else "Já sou cliente" if r < 0.55 else "")
    row = {c: "" for c in COLS_VER}
    row["Celular"] = tel
    row[CAMINHO_COL] = caminho
    if caminho:
        flow = FLOW_NOVO if caminho == "Sou novo por aqui" else FLOW_CLI
        thr  = THR_NOVO if caminho == "Sou novo por aqui" else THR_CLI
        # atendidos (q >= 0.67) passam do limiar do tipo de resíduo (0.65 novo / 0.43 cli)
        q = random.uniform(0.67, 1.0) if atendido else random.uniform(0.0, 0.97)
        for k, campo in enumerate(flow):
            if q >= thr[k]:
                preencher_campo(campo, idx, row)
    ver.append(row)
df_ver = pd.DataFrame(ver, columns=COLS_VER)

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
