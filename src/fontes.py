"""Carrega as tabelas que o painel tem direito de ler.

Mesma regra do projeto de auditoria: o gabarito não está na lista. No dia
a dia ninguém tem a resposta na mão, e um painel que consultasse o
gabarito mostraria uma operação que não existe.
"""

import sys

import pandas as pd

import config

COLUNAS_DE_DATA = {
    "data_emissao",
    "data_fim_vigencia",
    "data_vencimento",
    "data_pagamento",
    "data_criacao",
    "data",
    "cliente_desde",
}


def carregar(nome):
    if nome == config.NOME_GABARITO:
        raise PermissionError(
            "O painel não lê o gabarito. Ele mostra a operação como ela é "
            "vista no dia a dia, e no dia a dia ninguém tem a resposta."
        )
    if nome not in config.TABELAS:
        raise KeyError(f"'{nome}' não está na lista de fontes de config/fontes.yml")

    tabela = pd.read_csv(config.PASTA_BASE / f"{nome}.csv")
    for coluna in tabela.columns:
        if coluna in COLUNAS_DE_DATA:
            tabela[coluna] = pd.to_datetime(tabela[coluna], errors="coerce")
    return tabela


def carregar_tudo():
    if not config.PASTA_BASE.exists():
        print(
            "Não achei a base em:\n"
            f"  {config.PASTA_BASE}\n\n"
            "A base é gerada por outro projeto. Clone os dois lado a lado:\n\n"
            f"  git clone {config.FONTES['base']['repositorio']}\n"
            "  cd base-sintetica-seguros\n"
            "  pip install -r requirements.txt\n"
            "  python src/gerar_base.py\n\n"
            "Ou ajuste o caminho em config/fontes.yml.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    return {nome: carregar(nome) for nome in config.TABELAS}
