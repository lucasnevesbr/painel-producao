"""Monta o painel: lê a base, calcula, e escreve docs/index.html.

    python src/gerar_painel.py

O painel é uma página estática única, sem servidor, sem banco e sem
biblioteca externa. Motivo: ele não tem segredo para esconder nem
precisa de servidor rodando, então vai para o GitHub Pages e ganha URL
sozinho. Regra de deploy do portfólio.
"""

import json
from datetime import datetime

import config
import fontes
import metricas


def reais(valor):
    return (
        f"R$ {valor:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    )


def _cartao(item):
    return f"""      <div class="cartao">
        <span class="marca {item['papel']}"></span>
        <h2>{item['titulo']}</h2>
        <p class="regua">{item['regua']}</p>
        <div class="valor">{reais(item['valor'])}</div>
        <div class="detalhe">{item['detalhe']}</div>
      </div>"""


def _linha_seguradora(item, maior):
    proporcao = item["producao"] / maior * 100 if maior else 0
    return f"""      <tr>
        <td>
          <span class="nome">{item['nome']}</span>
          <div class="trilho"><div style="width: {proporcao:.1f}%"></div></div>
        </td>
        <td class="num" data-rotulo="Negócios">{item['negocios']}</td>
        <td class="num" data-rotulo="Produção">{reais(item['producao'])}</td>
        <td class="num" data-rotulo="Recebido">{reais(item['recebido'])}</td>
      </tr>"""


def _linha_consultor(item):
    return f"""      <tr>
        <td class="nome">{item['nome']}</td>
        <td class="num" data-rotulo="Negócios">{item['negocios']}</td>
        <td class="num" data-rotulo="Produção">{reais(item['producao'])}</td>
        <td class="num" data-rotulo="Ticket médio">{reais(item['ticket'])}</td>
      </tr>"""


def _linha_tomador(item):
    return f"""      <tr>
        <td class="nome">{item['nome']}</td>
        <td class="num" data-rotulo="Negócios">{item['negocios']}</td>
        <td class="num" data-rotulo="Produção">{reais(item['producao'])}</td>
      </tr>"""


def nota_do_consultor(dados):
    """O painel corrige o nome sujo, mas avisa que corrigiu.

    Esconder a correção faria o painel mentir de outro jeito: quem olha
    precisa saber que a base de origem tem esse problema, senão ele nunca
    é consertado na fonte.
    """
    quantidade = dados["nomes_corrigidos"]
    if not quantidade:
        return "Produção pela data da venda, que é a pergunta comercial: quem vendeu."

    return (
        "Produção pela data da venda, que é a pergunta comercial: quem vendeu. "
        f"<strong>{quantidade} linha(s) da planilha tinham espaço sobrando no nome "
        "do consultor</strong> e foram normalizadas aqui: sem isso, a mesma pessoa "
        "apareceria duas vezes e nenhum dos dois total estaria certo. "
        "O conserto de verdade é na origem."
    )


def main():
    base = fontes.carregar_tudo()
    dados = metricas.resumo(base)
    dados["empresa"] = config.EMPRESA["nome"]

    periodo = f"{dados['periodo']['inicio']} a {dados['periodo']['fim']}"
    maior = max(item["producao"] for item in dados["por_seguradora"])

    alt = (
        "Gráfico de barras da produção mês a mês. Cada mês tem duas barras: "
        "produção comercial, contada na data da venda, e comissão recebida, "
        "contada na data do pagamento."
    )

    modelo = (config.PASTA_MODELO / "painel.html").read_text(encoding="utf-8")
    pagina = (
        modelo.replace("__TITULO__", f"{config.EMPRESA['nome']} · Produção e comissões")
        .replace("__EMPRESA__", config.EMPRESA["nome"])
        .replace("__PERIODO__", periodo)
        .replace("__ALT_GRAFICO__", alt)
        .replace("__CARTOES__", "\n".join(_cartao(c) for c in dados["cartoes"]))
        .replace(
            "__SEGURADORAS__",
            "\n".join(_linha_seguradora(s, maior) for s in dados["por_seguradora"]),
        )
        .replace("__NOTA_CONSULTOR__", nota_do_consultor(dados))
        .replace(
            "__CONSULTORES__",
            "\n".join(_linha_consultor(c) for c in dados["por_consultor"]),
        )
        .replace(
            "__TOMADORES__",
            "\n".join(_linha_tomador(t) for t in dados["maiores_tomadores"]),
        )
        .replace("__GERADO_EM__", datetime.now().strftime("%d/%m/%Y"))
        .replace("__DADOS__", json.dumps(dados, ensure_ascii=False))
    )

    config.PASTA_PUBLICA.mkdir(exist_ok=True)
    destino = config.PASTA_PUBLICA / "index.html"
    destino.write_text(pagina, encoding="utf-8")

    print(f"Painel da {config.EMPRESA['nome']} gerado")
    print(f"  período            {periodo}")
    for cartao in dados["cartoes"]:
        print(f"  {cartao['titulo']:<19}{reais(cartao['valor']):>16}")
    print(f"  nomes normalizados {dados['nomes_corrigidos']:>16}")
    print(f"\n{destino}  ({destino.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
