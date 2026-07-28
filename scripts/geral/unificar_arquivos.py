# -*- coding: utf-8 -*-
"""
=====================================================================
 01 · UNIFICAÇÃO DOS ARQUIVOS DA TREBLE  (Nexforce · RevOps)
=====================================================================

OBJETIVO
--------
Pegar os arquivos soltos exportados da Treble na semana e juntá-los como ABAS
de um único arquivo .xlsx, no padrão que o script de análise espera.

Cada execução semanal costuma trazer estes tipos de arquivo:
  - 1 base de ATENDIMENTO por vendedor (Excel) ............ aba "atendimento-treble"
  - 1 LOG DE SESSÕES do fluxo (.csv OU .xlsx) ............. aba "sessoes-gerais"
  - 1..N relatórios de VERSÃO/qualificação (Excel) ........ abas "Versao 1", "Versao 2", ...
  - (opcional) 1 agregado de INBOX ....................... aba "inbox"

IMPORTANTE — NÚMERO DE VERSÕES É VARIÁVEL
-----------------------------------------
Uma semana pode ter 1 versão do fluxo ou 30. Este script NÃO assume um número
fixo: ele varre a pasta e cria uma aba "Versao N" para CADA arquivo de versão
encontrado. O script de análise, por sua vez, consolida TODAS as abas de versão
automaticamente (classifica pelas COLUNAS, não pelo nome da aba).

COMO USAR (modo automático — recomendado)
-----------------------------------------
1) Coloque todos os arquivos exportados da semana numa pasta (ex.: a pasta da
   semana criada pelo Organizador).
2) Rode:  python unificar_arquivos.py /caminho/da/pasta
   (sem argumento, usa a pasta atual ".")
3) Será gerado ARQUIVO_SAIDA com todas as abas, pronto para a análise.

MODO MANUAL (fallback)
----------------------
Se a descoberta automática não classificar algum arquivo (nome muito fora do
padrão), preencha a lista FONTES_MANUAIS no fim do arquivo e rode com:  --manual

REQUISITOS:  pandas, openpyxl   (pip install pandas openpyxl)
"""

import os
import re
import sys
import pandas as pd


# =====================================================================
# CONFIGURAÇÃO
# =====================================================================
ARQUIVO_SAIDA = "Dados_Treble_Semana.xlsx"

# Padrões de reconhecimento por NOME de arquivo (minúsculo). Ajuste se a
# convenção de exportação da Treble mudar.
PADRAO_SESSOES = ("session", "general_sessions")
PADRAO_VERSAO = ("fluxo", "relat", "nx 01", "nx_01", "conversacional")
PADRAO_ATENDIMENTO = ("treble",)        # base de atendimento por vendedor
PADRAO_INBOX = ("inbox",)
EXTENSOES_TABELA = (".xlsx", ".xlsm", ".xls", ".csv")


# =====================================================================
# LEITURA DE UM ARQUIVO (xlsx ou csv), de forma tolerante
# =====================================================================
def ler_arquivo(caminho, aba_interna=None):
    """Lê .xlsx (uma aba específica ou a primeira) ou .csv e devolve um DataFrame.
    Detecta o separador do CSV automaticamente."""
    ext = os.path.splitext(caminho)[1].lower()
    if ext in (".xlsx", ".xlsm", ".xls"):
        sheet = aba_interna if aba_interna is not None else 0
        return pd.read_excel(caminho, sheet_name=sheet)
    if ext == ".csv":
        df = pd.read_csv(caminho)
        if df.shape[1] == 1:           # veio tudo numa coluna -> tenta ';'
            df = pd.read_csv(caminho, sep=";")
        return df
    raise ValueError(f"Extensão não suportada: {ext} ({caminho})")


def _nome_aba_seguro(nome, usados):
    """Excel limita nome de aba a 31 caracteres e proíbe : \\ / ? * [ ].
    Também evita nomes duplicados."""
    limpo = re.sub(r'[:\\/?*\[\]]', " ", str(nome)).strip()[:31] or "aba"
    base, i = limpo, 2
    while limpo.lower() in {u.lower() for u in usados}:
        sufixo = f" ({i})"
        limpo = base[:31 - len(sufixo)] + sufixo
        i += 1
    return limpo


# =====================================================================
# DESCOBERTA AUTOMÁTICA DAS FONTES NA PASTA
# =====================================================================
def _classificar(nome_baixo):
    """Categoria do arquivo pelo nome: 'sessoes', 'inbox', 'versao',
    'atendimento' ou None. Ordem importa (sessões/inbox antes de 'treble')."""
    if any(p in nome_baixo for p in PADRAO_SESSOES):
        return "sessoes"
    if any(p in nome_baixo for p in PADRAO_INBOX):
        return "inbox"
    if any(p in nome_baixo for p in PADRAO_VERSAO):
        return "versao"
    if any(p in nome_baixo for p in PADRAO_ATENDIMENTO):
        return "atendimento"
    return None


def descobrir_fontes_da_pasta(pasta="."):
    """Varre a pasta e devolve a lista de FONTES (caminho, nome_aba, aba_interna),
    com UMA aba por arquivo de versão (sem número fixo de versões)."""
    fontes, n_versao = [], 0
    arquivos = sorted(
        f for f in os.listdir(pasta)
        if os.path.splitext(f)[1].lower() in EXTENSOES_TABELA
        and not f.startswith("~$")
        and os.path.abspath(os.path.join(pasta, f)) != os.path.abspath(ARQUIVO_SAIDA)
    )
    for nome in arquivos:
        cam = os.path.join(pasta, nome)
        cat = _classificar(nome.lower())
        if cat == "sessoes":
            fontes.append((cam, "sessoes-gerais", None))
        elif cat == "inbox":
            fontes.append((cam, "inbox", None))
        elif cat == "versao":
            n_versao += 1
            fontes.append((cam, f"Versao {n_versao}", None))
        elif cat == "atendimento":
            interna = None
            try:
                if os.path.splitext(nome)[1].lower() != ".csv":
                    abas = pd.ExcelFile(cam).sheet_names
                    interna = "treble (2)" if "treble (2)" in abas else abas[0]
            except Exception:
                interna = None
            fontes.append((cam, "atendimento-treble", interna))
        else:
            print(f"[aviso] arquivo não classificado (ignorado): {nome}")
    return fontes


# =====================================================================
# UNIFICAÇÃO
# =====================================================================
def unificar(fontes, saida=ARQUIVO_SAIDA):
    if not fontes:
        raise SystemExit("Nenhuma fonte encontrada — verifique a pasta/arquivos.")
    usados, escritos, n_versoes = [], 0, 0
    with pd.ExcelWriter(saida, engine="openpyxl") as writer:
        for item in fontes:
            caminho, nome_aba = item[0], item[1]
            aba_interna = item[2] if len(item) > 2 else None
            if not os.path.exists(caminho):
                print(f"[aviso] arquivo não encontrado, pulando: {caminho}")
                continue
            try:
                df = ler_arquivo(caminho, aba_interna)
            except Exception as e:
                print(f"[erro] falha ao ler {caminho}: {e}")
                continue
            aba = _nome_aba_seguro(nome_aba, usados)
            usados.append(aba)
            if aba.lower().startswith("versao"):
                n_versoes += 1
            import re as _re
            _illegal = _re.compile(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]')
            _clean = lambda v: _illegal.sub('', v) if isinstance(v, str) else v
            try:
                df = df.map(_clean)
            except TypeError:
                df = df.applymap(_clean)
            df.to_excel(writer, sheet_name=aba, index=False)
            escritos += 1
            print(f"[ok] '{os.path.basename(caminho)}'  ->  aba '{aba}'  "
                  f"({len(df)} linhas, {df.shape[1]} colunas)")
    if escritos == 0:
        raise SystemExit("Nenhuma aba foi escrita — verifique os caminhos/fontes.")
    print(f"\n[concluído] {escritos} aba(s) gravada(s) "
          f"({n_versoes} versão(ões) do fluxo) em: {saida}")
    abas_nomes = [u.lower() for u in usados]
    if not any("atendimento" in a for a in abas_nomes):
        print("[ALERTA] não foi gravada a aba de ATENDIMENTO (base de verdade).")
    if not any("sess" in a for a in abas_nomes):
        print("[ALERTA] não foi gravada a aba de SESSÕES.")
    if n_versoes == 0:
        print("[ALERTA] nenhuma aba de VERSÃO do fluxo foi gravada.")
    return saida


# =====================================================================
# FONTES MANUAIS (fallback) — só usadas com --manual
# =====================================================================
FONTES_MANUAIS = [
    # (caminho, nome_da_aba, aba_interna_ou_None)
    # ("treble.xlsx", "atendimento-treble", "treble (2)"),
    # ("general_sessions_report.xlsx", "sessoes-gerais", None),
    # ("NX_01_..._1.xlsx", "Versao 1", None),
    # ("NX_01_..._2.xlsx", "Versao 2", None),
]


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--manual" in args:
        unificar(FONTES_MANUAIS)
    else:
        pasta = next((a for a in args if not a.startswith("-")), ".")
        print(f">>> Descoberta automática na pasta: {os.path.abspath(pasta)}")
        unificar(descobrir_fontes_da_pasta(pasta))
