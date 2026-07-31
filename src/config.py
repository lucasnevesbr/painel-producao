"""Lê config/empresa.yml e config/fontes.yml."""

from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
PASTA_CONFIG = RAIZ / "config"
PASTA_MODELO = RAIZ / "modelo"

# O painel gerado vai para docs/, porque é de lá que o GitHub Pages serve.
PASTA_PUBLICA = RAIZ / "docs"


def _ler(nome_arquivo):
    with open(PASTA_CONFIG / nome_arquivo, encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo)


_empresa = _ler("empresa.yml")
FONTES = _ler("fontes.yml")

EMPRESA = _empresa["empresa"]
SINTETICO = _empresa["dados"]["sintetico"]

if not SINTETICO:
    raise RuntimeError(
        "config/empresa.yml está com sintetico: false. "
        "Dado real não roda em repositório público. "
        "Torne o repositório privado antes de mudar essa chave."
    )

PASTA_BASE = (RAIZ / FONTES["base"]["caminho"]).resolve()
TABELAS = FONTES["tabelas"]
NOME_GABARITO = FONTES["gabarito"]
