"""Calcula os números do painel.

Regra que governa este arquivo inteiro: **as duas réguas nunca se
misturam.**

    PRODUÇÃO COMERCIAL   contrato cheio, na data da venda      (fonte: CRM)
    COMISSÃO RECEBIDA    parcela paga, na data do pagamento    (fonte: financeiro)

Cada número carrega o nome da régua que usou, e nenhuma função aqui
subtrai uma da outra. Foi essa subtração que fez a diretoria procurar
R$ 630 mil que nunca estiveram faltando.

Ver: https://github.com/lucasnevesbr/auditoria-comissoes
"""

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def _reais(valor):
    return round(float(valor), 2)


def limpar_consultor(planilha):
    """Tira espaço sobrando do nome do consultor, e conta quantos tinham.

    "Julia " e "Julia" são pessoas diferentes para qualquer soma agrupada.
    O painel corrige em vez de exibir o total errado, mas avisa que
    corrigiu: esconder o problema faria o painel mentir de outro jeito.
    """
    planilha = planilha.copy()
    original = planilha["consultor"].astype(str)
    planilha["consultor"] = original.str.strip()
    return planilha, int((original != planilha["consultor"]).sum())


def resumo(base):
    crm = base["crm_negocios"]
    planilha, nomes_corrigidos = limpar_consultor(base["planilha_producao"])

    recebidas = planilha[planilha["status_comissao"] == "Recebido"]
    pendentes = planilha[planilha["status_comissao"] == "Pendente"]
    canceladas = planilha[planilha["status_boleto"] == "Cancelado"]

    return {
        "empresa": None,  # preenchido em gerar_painel
        "periodo": {
            "inicio": crm["data_criacao"].min().strftime("%d/%m/%Y"),
            "fim": crm["data_criacao"].max().strftime("%d/%m/%Y"),
        },
        "cartoes": [
            {
                "titulo": "Produção comercial",
                "regua": "contrato cheio, na data da venda",
                "valor": _reais(crm["valor_comissao"].sum()),
                "detalhe": f"{len(crm)} negócios fechados",
                "papel": "comercial",
            },
            {
                "titulo": "Comissão recebida",
                "regua": "parcela paga, na data do pagamento",
                "valor": _reais(recebidas["valor_comissao"].sum()),
                "detalhe": f"{len(recebidas)} parcelas liquidadas",
                "papel": "financeiro",
            },
            {
                "titulo": "A receber",
                "regua": "parcela que ainda não venceu",
                "valor": _reais(pendentes["valor_comissao"].sum()),
                "detalhe": f"{len(pendentes)} parcelas em aberto",
                "papel": "financeiro",
            },
        ],
        "cancelado": {
            "valor": _reais(canceladas["valor_comissao"].sum()),
            "quantidade": int(canceladas["numero_apolice"].nunique()),
        },
        "nomes_corrigidos": nomes_corrigidos,
        "por_mes": por_mes(crm, recebidas),
        "por_seguradora": por_seguradora(crm, planilha),
        "por_consultor": por_consultor(crm, planilha),
        "maiores_tomadores": maiores_tomadores(crm),
    }


def por_mes(crm, recebidas):
    """Duas séries, cada uma com a data que lhe é própria.

    Elas aparecem lado a lado no painel, nunca subtraídas, e a legenda
    diz qual data cada uma usa.
    """
    comercial = crm.groupby(crm["data_criacao"].dt.month)["valor_comissao"].sum()
    recebido = recebidas.groupby(recebidas["data_pagamento"].dt.month)[
        "valor_comissao"
    ].sum()

    return [
        {
            "mes": MESES[mes - 1],
            "comercial": _reais(comercial.get(mes, 0)),
            "recebido": _reais(recebido.get(mes, 0)),
        }
        for mes in range(1, 13)
    ]


def por_seguradora(crm, planilha):
    producao = crm.groupby("seguradora")["valor_comissao"].sum()
    recebido = (
        planilha[planilha["status_comissao"] == "Recebido"]
        .groupby("seguradora")["valor_comissao"]
        .sum()
    )
    negocios = crm.groupby("seguradora").size()
    total = producao.sum()

    linhas = [
        {
            "nome": nome,
            "producao": _reais(valor),
            "recebido": _reais(recebido.get(nome, 0)),
            "negocios": int(negocios.get(nome, 0)),
            "participacao": round(float(valor / total * 100), 1),
        }
        for nome, valor in producao.items()
    ]
    return sorted(linhas, key=lambda linha: linha["producao"], reverse=True)


def por_consultor(crm, planilha):
    """Produção por consultor, com o nome já limpo.

    A produção vem do CRM porque a pergunta é comercial: quem vendeu.
    Misturar com recebimento aqui responderia outra pergunta e é
    justamente o tipo de mistura que este painel evita.
    """
    del planilha
    producao = crm.groupby("consultor")["valor_comissao"].sum()
    negocios = crm.groupby("consultor").size()
    ticket = producao / negocios

    linhas = [
        {
            "nome": nome,
            "producao": _reais(valor),
            "negocios": int(negocios[nome]),
            "ticket": _reais(ticket[nome]),
        }
        for nome, valor in producao.items()
    ]
    return sorted(linhas, key=lambda linha: linha["producao"], reverse=True)


def maiores_tomadores(crm, quantidade=8):
    producao = crm.groupby("tomador")["valor_comissao"].sum()
    negocios = crm.groupby("tomador").size()

    linhas = [
        {
            "nome": nome,
            "producao": _reais(valor),
            "negocios": int(negocios[nome]),
        }
        for nome, valor in producao.items()
    ]
    ordenadas = sorted(linhas, key=lambda linha: linha["producao"], reverse=True)
    return ordenadas[:quantidade]
