# painel-producao

> **Uma página que o dono da corretora abre no celular e entende em dez segundos**, sem planilha, sem login e sem pedir relatório pra ninguém.
>
> É a terceira parte de um conjunto: a [base](https://github.com/Lucasnevesads/base-sintetica-seguros) cria o dado, a [auditoria](https://github.com/Lucasnevesads/auditoria-comissoes) confere, e este painel apresenta.

![Dados sintéticos](https://img.shields.io/badge/dados-sintéticos-7C3AED?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)
![Sem dependência no navegador](https://img.shields.io/badge/navegador-zero_biblioteca-16A34A?style=flat-square)

![Topo do painel da Norte Garantia. Título, período de 01/01/2025 a 31/12/2025 e um selo de dados sintéticos. Abaixo, um aviso destacado explicando que o painel usa duas réguas e nunca as subtrai. Em seguida, três cartões: produção comercial de R$ 4.080.660,80 em 791 negócios, comissão recebida de R$ 3.450.030,87 em 1.307 parcelas, e a receber de R$ 446.084,93 em 229 parcelas.](docs/print.png)

🔗 **Ver funcionando:** https://lucasnevesads.github.io/painel-producao/

A imagem é o tema claro. A página também tem tema escuro, escolhido e não invertido, que aparece sozinho se o seu sistema estiver nele.

---

## O problema

Todo mês alguém do comercial pede o número da produção, alguém do financeiro manda outro número, e os dois estão certos. Aí a diretoria compara os dois, encontra uma diferença de R$ 630 mil e o mês inteiro vira reunião sobre um dinheiro que nunca sumiu.

A causa é sempre a mesma: **o CRM conta o contrato cheio na data da venda, o banco conta a parcela na data em que ela cai.** São réguas diferentes.

Um painel que joga os dois números lado a lado sem dizer isso não resolve o problema. Ele automatiza o problema.

> **Essa reunião não é hipotética.** Separar os dois indicadores nos relatórios, e nunca subtrair um do outro, foi a primeira recomendação que eu fiz depois de conferir o fechamento de uma corretora de seguro garantia de verdade, onde trabalho. Este painel é essa recomendação construída.

## O que eu fiz

Uma página estática única, gerada em Python a partir da base da Norte Garantia, que mostra produção, recebimento, seguradoras, consultores e maiores clientes.

Quatro decisões que não eram óbvias:

**1. Painel próprio em vez de Power BI ou Looker Studio.** A pergunta certa não é qual ferramenta é mais poderosa, é de que jeito aquela diretoria recebe melhor a informação. Ferramenta de BI entrega o layout dela e o vocabulário dela. Um painel próprio entrega o recorte que a diretoria já está acostumada a ler, com o aviso das duas réguas exatamente onde ele precisa estar.

É escolha de contexto, não regra geral: ferramenta de BI ganha fácil quando o dado atualiza sozinho, quando muita gente precisa fatiar por conta própria ou quando não há ninguém para manter código. **A hora de trocar é quando começarem a pedir filtro.**

O que torna essa decisão reversível é a próxima: as tabelas de origem seguem em formato longo, um grão por arquivo, data em ISO e nada de significado escondido em cor ou em nome de aba. A mesma base sobe no Power BI, no Looker Studio ou num Postgres sem tratamento nenhum. **O painel é a apresentação; a estrutura do dado é a fundação, e ela continua portátil.**

**2. As duas réguas nunca se subtraem, e isso é regra do código.** Cada número carrega o nome da régua que usou, e nenhuma função em `src/metricas.py` cruza uma com a outra. O aviso no topo da página explica a diferença em duas frases, antes de qualquer valor aparecer. O painel foi desenhado para que o erro da auditoria não possa acontecer de novo.

**3. Nenhuma biblioteca no navegador.** O gráfico é SVG escrito na mão, com tooltip e navegação por teclado. Sem CDN, sem framework de dashboard, sem rastreador. A página inteira tem 22 KB e abre em qualquer celular, inclusive com internet ruim, que é a realidade de quem vai abrir isso.

**4. O painel corrige o nome sujo, mas avisa que corrigiu.** Cinco linhas da planilha têm espaço sobrando no nome do consultor, e sem tratar isso a mesma pessoa apareceria duas vezes. O painel normaliza e escreve, na própria seção, que normalizou e quantas linhas. Corrigir em silêncio faria o painel mentir de outro jeito: o problema nunca chegaria a quem pode consertá-lo na origem.

## O resultado

Página no ar, 22 KB, sem servidor e sem banco:

| | |
|---|---|
| Produção comercial | R$ 4.080.660,80 · 791 negócios |
| Comissão recebida | R$ 3.450.030,87 · 1.307 parcelas |
| A receber | R$ 446.084,93 · 229 parcelas |

**Verificado no celular primeiro**, em 375px de largura: nenhum elemento vaza a tela, as tabelas de quatro colunas viram lista empilhada com os valores rotulados, e o gráfico rola dentro da própria caixa em vez de arrastar a página. Modo escuro é escolhido, não invertido: contraste de 19,4:1 no texto principal e 4,8:1 nas barras contra a superfície escura.

## Como rodar

A base vem de outro projeto. Clone os dois lado a lado:

```bash
git clone https://github.com/Lucasnevesads/base-sintetica-seguros
cd base-sintetica-seguros && pip install -r requirements.txt && python src/gerar_base.py && cd ..

git clone https://github.com/Lucasnevesads/painel-producao
cd painel-producao
pip install -r requirements.txt
python src/gerar_painel.py
```

Sai `docs/index.html`, que é o que o GitHub Pages serve. Para ver localmente, abra o arquivo no navegador: não precisa de servidor.

---

## 🔍 Detalhe técnico

### Por que estático

A régua de deploy do portfólio: se não tem segredo para esconder nem precisa de servidor rodando, vai para o GitHub Pages e ganha URL sozinho.

Este painel lê CSV e escreve HTML. Não tem login, não tem banco, não tem chave de API. Colocar isso numa VPS seria pagar servidor para servir um arquivo.

O efeito colateral é bom: a página não tem como cair, não tem como vazar dado e não tem como ficar lenta.

### O gráfico, escrito na mão

12 meses × 2 séries, em SVG gerado por JavaScript a partir do JSON embutido na página.

- Paleta validada com o script da skill de dataviz: azul `#2a78d6` e laranja `#eb6834` no claro, `#3987e5` e `#d95926` no escuro. Separação sob daltonismo ΔE 24,7 e 26,8, contra um alvo de 8.
- Legenda sempre presente, porque são duas séries, e cada entrada diz **qual data** aquela série usa. Sem isso a legenda seria decorativa.
- Tooltip no `pointerenter` e também no `focus`, com `tabindex` em cada grupo de mês e `aria-label` com os dois valores. Quem navega por teclado ou leitor de tela recebe a mesma informação.
- Grade recuada, eixo sem marcações, barras finas com cantos arredondados. O dado é que tem que aparecer.

### Mobile-first de verdade

O CSS começa no celular e só acrescenta espaço acima de 620px, nunca o contrário.

O ponto que deu trabalho foram as tabelas. Quatro colunas em 375px estouram a tela e forçam a página a rolar de lado, que é o pior jeito possível de ler número. Abaixo de 620px cada linha vira um bloco: nome em cima, valores rotulados embaixo via `data-rotulo` no CSS. O gráfico segue outra estratégia, rolando dentro da própria caixa, porque comprimir doze meses em 375px tornaria os rótulos ilegíveis.

Medido no navegador, não no olho: em 375px, zero elementos com largura maior que a viewport.

### Limitações

- **O painel é uma fotografia, não um sistema.** Ele é regerado rodando um comando. Não atualiza sozinho, não tem filtro de período e não tem seleção de mês. Para isso seria preciso servidor, e aí a régua de deploy muda.
- **Não há autenticação.** É informação de uma empresa fictícia, então tudo bem. Com dado real, a página inteira precisaria de outra arquitetura, não de uma senha por cima.
- **O gráfico rola de lado no celular.** É a escolha menos ruim entre rolar e não conseguir ler, mas continua sendo atrito.
- **Os números por consultor usam o nome normalizado.** Se duas pessoas diferentes tiverem exatamente o mesmo nome, elas viram uma só, e o painel não tem como saber.
- **Não conferi visualmente em aparelho real.** A verificação foi medida no navegador (largura, empilhamento, contraste, tooltip, teclado), o que pega layout quebrado mas não pega "ficou feio".

---

## 🧪 Sobre os dados

Os dados são da **Norte Garantia**, uma corretora de seguro garantia **fictícia**, gerada em [`base-sintetica-seguros`](https://github.com/Lucasnevesads/base-sintetica-seguros). As seguradoras também são fictícias.

Nenhum dado de cliente ou de empresa real é usado, em nenhuma etapa.

O nome da empresa fica isolado em [`config/empresa.yml`](config/empresa.yml). O código tem uma trava: se alguém mudar `sintetico: true` para `false`, o projeto para de rodar.

Como o painel também não lê o gabarito de defeitos da base, ele mostra a operação como ela é vista no dia a dia, que é sem a resposta na mão.

---

## 📄 Documentação

- [`docs/decisoes.md`](docs/decisoes.md) · por que cada escolha foi feita, e o que ela custou
