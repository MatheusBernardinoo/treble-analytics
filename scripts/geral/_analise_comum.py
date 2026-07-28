# -*- coding: utf-8 -*-
"""
=====================================================================
 LÓGICA COMUM DE ANÁLISE — Treble
 Nexforce | RevOps
=====================================================================

Fonte ÚNICA das funções de metodologia das seções 05 (padrão de resíduo)
e 06 (preenchimento por caminho), importada pelos scripts de análise:

  - scripts/geral/analise_treble_semanal.py
  - scripts/geral/analise_equipe_periodo.py

Centralizar aqui garante que qualquer ajuste de metodologia valha para
todos os scripts que importam este módulo, sem divergência entre cópias.

REGRAS PERMANENTES (ver CLAUDE.md § REGRAS PERMANENTES DE ANÁLISE):
  - Seção 05: Industrial e Hospitalar segmentados por classe; classes com
    0 contatos aparecem na TABELA (não no gráfico de pizza).
  - Seção 06: o caminho de cada sessão vem da PRIMEIRA PERGUNTA do fluxo
    (coluna "...você é novo por aqui ou já é cliente?"), com valores
    "Sou novo por aqui", "Já sou cliente" ou vazio. A taxa de preenchimento
    de cada caminho usa como DENOMINADOR a contagem de sessões DAQUELE
    caminho (não o total da semana). Sessões em branco (não entraram em
    nenhum caminho) são excluídas da completude por caminho.
    "Sou novo por aqui" mostra 10 campos; "Já sou cliente" mostra 6 campos
    (email, nome, cpf/cnpj, tipo_residuo, qtd_residuo, tipo_servico) —
    os demais não são coletados nesse caminho.

Este módulo é autocontido (define os poucos helpers que as funções usam)
para não reintroduzir acoplamento com a configuração de cada script.
"""

import re
import unicodedata
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# Helpers de base (cópia estável; idênticos em todos os scripts)
# ---------------------------------------------------------------------

def corrigir_mojibake(s):
    if isinstance(s, str) and ("Ã" in s or "Â" in s):
        try:
            return s.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return s
    return s


def _norm(txt):
    txt = corrigir_mojibake(str(txt))
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", txt.lower())


def achar_coluna(df, *candidatos):
    mapa = {_norm(c): c for c in df.columns}
    for cand in candidatos:
        chave = _norm(cand)
        if chave in mapa:
            return mapa[chave]
        for k, real in mapa.items():
            if chave in k or k in chave:
                return real
    return None


def nucleo_telefone(num):
    d = re.sub(r"\D", "", str(num))
    if len(d) >= 12 and d.startswith("55"):
        d = d[2:]
    return d


# ---------------------------------------------------------------------
# SEÇÃO 05 — PADRÃO DE RESÍDUO
# ---------------------------------------------------------------------

# Sub-categorias esperadas por tipo — garante linhas 0% na tabela quando o tipo existe
_CATS_RESIDUO = {
    "Hospitalar": [
        "Hospitalar · Perigoso (Classe 1)",
        "Hospitalar · Não perigoso (Classe 2)",
        "Hospitalar · Não sei informar",
        "Hospitalar · classe não informada",
    ],
    "Industrial": [
        "Industrial · Perigoso (Classe 1)",
        "Industrial · Não perigoso (Classe 2)",
        "Industrial · Não sei informar",
        "Industrial · classe não informada",
    ],
}


def _classificar_padrao_residuo(tipo, classe):
    """Deriva o 'padrão de resíduo' de um contato a partir do tipo e da classe
    informados no fluxo. Industrial e Hospitalar são segmentados por classe."""
    t = "" if pd.isna(tipo) else str(tipo).strip().lower()
    c = "" if pd.isna(classe) else str(classe).strip().lower()
    if "industr" in t:
        if "perigoso" in c and "nao" not in c.replace("ã", "a") and "não" not in c:
            return "Industrial · Perigoso (Classe 1)"
        if "perigoso" in c:
            return "Industrial · Não perigoso (Classe 2)"
        if "sei" in c or "nao sei" in c.replace("ã", "a"):
            return "Industrial · Não sei informar"
        return "Industrial · classe não informada"
    if "hospital" in t:
        if "perigoso" in c and "nao" not in c.replace("ã", "a") and "não" not in c:
            return "Hospitalar · Perigoso (Classe 1)"
        if "perigoso" in c:
            return "Hospitalar · Não perigoso (Classe 2)"
        if "sei" in c or "nao sei" in c.replace("ã", "a"):
            return "Hospitalar · Não sei informar"
        return "Hospitalar · classe não informada"
    if t:
        return "Outro tipo informado"
    return "Tipo não informado"


def padrao_residuo_atribuidos(at, v):
    """Para cada contato que chegou a um vendedor (base atendimento), busca o
    tipo/classe de resíduo informado no fluxo (versões) pelo núcleo de telefone
    e devolve: composição por padrão + respondidas x sem resposta por padrão.
    Retorna {} se faltar a base de versões ou a coluna de classe."""
    base = at[at["agente"].notna()].copy()
    if not len(base) or not len(v):
        return {}
    col_tipo = achar_coluna(v, "hubspot_tipo_de_residuo")
    col_classe = achar_coluna(v, "hubspot_truora_classe_residuo")
    if not col_tipo and not col_classe:
        return {}
    vv = v.copy()
    vv["nucleo"] = vv["telefone"].map(nucleo_telefone)
    # uma linha por núcleo, priorizando registros com tipo/classe preenchidos
    vv["_score"] = (vv[col_tipo].notna() if col_tipo else 0).astype(int) + \
                   (vv[col_classe].notna() if col_classe else 0).astype(int)
    vv = vv.sort_values("_score", ascending=False).drop_duplicates("nucleo", keep="first")
    cols_keep = ["nucleo"] + [c for c in [col_tipo, col_classe] if c]
    base = base.merge(vv[cols_keep], on="nucleo", how="left", suffixes=("", "_v"))
    base["padrao"] = base.apply(
        lambda r: _classificar_padrao_residuo(
            r.get(col_tipo) if col_tipo else None,
            r.get(col_classe) if col_classe else None), axis=1)

    # composição (contagem por padrão)
    comp = (base["padrao"].value_counts(dropna=False)
            .rename_axis("padrao").reset_index(name="contatos"))
    comp["%"] = round(100 * comp["contatos"] / len(base), 1)

    # respondidas x sem resposta por padrão (volume)
    grp = base.groupby("padrao").agg(
        contatos=("padrao", "size"),
        respondidos=("respondido", "sum"),
    ).reset_index()
    grp["respondidos"] = grp["respondidos"].astype(int)
    grp["sem_resposta"] = grp["contatos"] - grp["respondidos"]
    grp["%_sem_resposta"] = round(100 * grp["sem_resposta"] / grp["contatos"], 1)
    grp["%_respondida"] = round(100 * grp["respondidos"] / grp["contatos"], 1)
    # tempo mediano de resposta por padrão (apenas conversas respondidas)
    if "tempo_1a_resposta_h" in base.columns:
        resp_base = base[base["respondido"] == True]
        tempo_med = resp_base.groupby("padrao")["tempo_1a_resposta_h"].median().round(2)
        grp["tempo_mediano_resp"] = grp["padrao"].map(tempo_med)
    else:
        grp["tempo_mediano_resp"] = np.nan
    # garante que todas as sub-categorias de tipos presentes aparecem na TABELA (grp),
    # mesmo com 0 contatos — o gráfico de pizza (comp) só exibe categorias > 0.
    for tipo, cats in _CATS_RESIDUO.items():
        if grp["padrao"].str.startswith(tipo).any():
            extras = []
            for cat in cats:
                if cat not in grp["padrao"].values:
                    extras.append({
                        "padrao": cat, "contatos": 0,
                        "respondidos": 0, "sem_resposta": 0,
                        "%_sem_resposta": 0.0, "%_respondida": 0.0,
                    })
            if extras:
                grp = pd.concat([grp, pd.DataFrame(extras)], ignore_index=True)

    # reordena: tipos com mais contatos primeiro; dentro do tipo, sub-categorias por contato
    grp["_tipo"] = grp["padrao"].apply(lambda x: x.split(" · ")[0] if " · " in str(x) else x)
    grp["_vol_tipo"] = grp.groupby("_tipo")["contatos"].transform("sum")
    grp = (grp.sort_values(["_vol_tipo", "_tipo", "contatos"], ascending=[False, True, False])
           .drop(columns=["_tipo", "_vol_tipo"]).reset_index(drop=True))
    return {"composicao": comp, "resposta_por_padrao": grp}


# ---------------------------------------------------------------------
# SEÇÃO 06 — PREENCHIMENTO DOS CAMPOS POR CAMINHO
# ---------------------------------------------------------------------

def _achar_coluna_caminho(v):
    """Acha a coluna da PRIMEIRA PERGUNTA do fluxo, cujos valores são exatamente
    'Sou novo por aqui' ou 'Já sou cliente'. Escolhe a coluna com MAIS células que
    casam exatamente com uma das duas opções (compara pela versão normalizada,
    robusto a mojibake). O match exato evita falsos positivos de colunas que só
    contêm o texto como substring — ex.: estado interno do bot em JSON ou e-mail."""
    # DEPENDÊNCIA FRÁGIL: se a Treble reescrever o texto da primeira pergunta, o
    # valor não normaliza mais para "sounovoporaqui"/"jasoucliente", o score fica
    # 0 e esta função retorna None — a seção 06 sai VAZIA em silêncio. Se as abas
    # G2b/G2c vierem vazias numa execução, suspeitar primeiro do texto desta opção.
    melhor, melhor_score = None, 0
    for c in v.columns:
        vals = v[c].dropna().astype(str).map(_norm)
        score = int(vals.eq("sounovoporaqui").sum() + vals.eq("jasoucliente").sum())
        if score > melhor_score:
            melhor, melhor_score = c, score
    return melhor if melhor_score > 0 else None


# Ordem REAL das perguntas em cada caminho do fluxo (a mesma dos gráficos
# G2b/G2c e das leituras de quedas do relatório):
FLOW_NOVO = ["email", "nome", "empresa", "cpf/cnpj", "estado", "cidade",
             "classe_residuo", "tipo_residuo", "qtd_residuo", "tipo_servico"]
FLOW_CLI  = ["email", "nome", "cpf/cnpj", "tipo_residuo", "qtd_residuo", "tipo_servico"]


def analise_caminhos(v):
    v = v.copy()
    # O caminho de cada sessão vem da coluna da PRIMEIRA PERGUNTA do fluxo
    # ("...você é novo por aqui ou já é cliente?"): "Sou novo por aqui",
    # "Já sou cliente" ou vazio (não respondeu).
    col_caminho = _achar_coluna_caminho(v)
    if col_caminho is not None:
        norm_path = v[col_caminho].map(lambda x: _norm(x) if pd.notna(x) else "")
    else:
        norm_path = pd.Series("", index=v.index)
    novo_mask = norm_path.eq("sounovoporaqui")
    cli_mask = norm_path.eq("jasoucliente")

    v["caminho"] = np.select(
        [novo_mask, cli_mask],
        ["Sou novo por aqui", "Já sou cliente"],
        default="Não informou (sem caminho)")
    cd = v["caminho"].value_counts(dropna=False).rename_axis("caminho").reset_index(name="conversas")
    cd["%"] = round(100 * cd["conversas"] / len(v), 1) if len(v) else 0

    # Completude geral (todos os campos, sobre todas as sessões) — aba auxiliar G2.
    campos = {"email": "hubspot_email", "nome": "hubspot_firstname", "empresa": "hubspot_company",
              "estado": "hubspot_state",
              "cidade": "hubspot_city", "tipo_residuo": "hubspot_tipo_de_residuo",
              "classe_residuo": "hubspot_truora_classe_residuo",
              "qtd_residuo": "hubspot_truora_quantidade_residuo",
              "tipo_servico": "hubspot_truora_tipo_de_servico"}
    comp = []
    for rot, nc in campos.items():
        real = achar_coluna(v, nc); pr = int(v[real].notna().sum()) if real else 0
        comp.append((rot, pr, round(100 * pr / len(v), 1) if len(v) else 0))
    col_cpf = achar_coluna(v, "hubspot_cpf"); col_cnpj = achar_coluna(v, "hubspot_cnpj")
    tem_cpf = v[col_cpf].notna() if col_cpf else pd.Series(False, index=v.index)
    tem_cnpj = v[col_cnpj].notna() if col_cnpj else pd.Series(False, index=v.index)
    pr_doc = int((tem_cpf | tem_cnpj).sum())
    comp.append(("cpf/cnpj", pr_doc, round(100 * pr_doc / len(v), 1) if len(v) else 0))
    completude = pd.DataFrame(comp, columns=["campo", "preenchidos", "%_preenchido"])

    # Campos COLETADOS por caminho (CPF/CNPJ unificado é somado à parte):
    # "Sou novo por aqui" coleta os 10; "Já sou cliente" coleta só 6.
    campos_novo = {
        "email": "hubspot_email", "nome": "hubspot_firstname",
        "empresa": "hubspot_company", "estado": "hubspot_state",
        "cidade": "hubspot_city", "classe_residuo": "hubspot_truora_classe_residuo",
        "tipo_residuo": "hubspot_tipo_de_residuo",
        "qtd_residuo": "hubspot_truora_quantidade_residuo",
        "tipo_servico": "hubspot_truora_tipo_de_servico",
    }
    campos_cli = {
        "email": "hubspot_email", "nome": "hubspot_firstname",
        "tipo_residuo": "hubspot_tipo_de_residuo",
        "qtd_residuo": "hubspot_truora_quantidade_residuo",
        "tipo_servico": "hubspot_truora_tipo_de_servico",
    }

    def _completude_caminho(sub, campo_dict, ordem_fluxo):
        """Taxa de preenchimento de cada campo DENTRO do caminho — denominador é
        o número de sessões do próprio caminho (len(sub)). As linhas saem na
        ORDEM REAL das perguntas no fluxo (ordem_fluxo), para que gráficos e
        leituras de quedas contem a mesma história."""
        n = len(sub)
        if n == 0:
            return pd.DataFrame(columns=["campo", "preenchidos", "%_preenchido"])
        rows = []
        for rot, nc in campo_dict.items():
            real = achar_coluna(sub, nc); pr = int(sub[real].notna().sum()) if real else 0
            rows.append((rot, pr, round(100 * pr / n, 1)))
        c_cpf = achar_coluna(sub, "hubspot_cpf"); c_cnpj = achar_coluna(sub, "hubspot_cnpj")
        t_cpf = sub[c_cpf].notna() if c_cpf else pd.Series(False, index=sub.index)
        t_cnpj = sub[c_cnpj].notna() if c_cnpj else pd.Series(False, index=sub.index)
        pr_d = int((t_cpf | t_cnpj).sum())
        rows.append(("cpf/cnpj", pr_d, round(100 * pr_d / n, 1)))
        df = pd.DataFrame(rows, columns=["campo", "preenchidos", "%_preenchido"])
        pos = {c: i for i, c in enumerate(ordem_fluxo)}
        return (df.sort_values(by="campo", key=lambda s: s.map(lambda c: pos.get(c, len(pos))))
                  .reset_index(drop=True))

    novo = v[novo_mask]
    cli = v[cli_mask]
    comp_novo = _completude_caminho(novo, campos_novo, FLOW_NOVO)
    comp_cli = _completude_caminho(cli, campos_cli, FLOW_CLI)
    n_novo = int(novo_mask.sum())
    n_cli = int(cli_mask.sum())
    n_total = len(v)

    return {
        "distribuicao_caminho": cd,
        "completude_qualificacao": completude,
        "completude_novo": comp_novo,
        "completude_cli": comp_cli,
        "n_sessoes_novo": n_novo,
        "n_sessoes_cli": n_cli,
        "n_sessoes_total": n_total,
    }
