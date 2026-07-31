# Decisões do projeto

Registro do **porquê**, não do que foi feito. O código já mostra o que foi feito.

---

## 31/07/2026 · As duas réguas nunca se subtraem, e isso é regra do código

**Situação:** o jeito normal de fazer um painel de produção é botar "vendido" e "recebido" lado a lado e, quase sempre, mostrar a diferença como se fosse um indicador.

**Alternativas:** mostrar a diferença como um KPI, ou proibir a subtração.

**Escolhi:** proibir. Nenhuma função de `src/metricas.py` cruza as duas réguas, cada número carrega o nome da régua que usou, e o aviso no topo da página explica a diferença antes de qualquer valor aparecer.

O motivo é que a diferença **não é um indicador**. Ela é a distância entre a data da venda e a data do pagamento, e mostrá-la como número faz o leitor achar que é dinheiro faltando. Foi exatamente esse erro que a [auditoria](https://github.com/Lucasnevesads/auditoria-comissoes) desmontou. Um painel que reproduz o erro automatiza o problema em vez de resolvê-lo.

**Custo:** o painel deixa de responder "quanto falta entrar do que já foi vendido", que é uma pergunta legítima. A resposta certa exigiria cruzar por cronograma de parcelas, não por total, e isso é trabalho de outro projeto. Preferi não responder a responder errado.

---

## 31/07/2026 · Nenhuma biblioteca no navegador

**Situação:** existem bibliotecas de gráfico prontas, e o gráfico sairia em vinte linhas.

**Alternativas:** carregar uma biblioteca por CDN, empacotar uma no repositório, ou escrever o SVG na mão.

**Escolhi:** escrever na mão. A página tem 22 KB no total e não faz nenhuma requisição externa.

Três motivos, em ordem de peso: **CDN é uma porta** que eu não controlo, no mesmo raciocínio que vale para dependência de servidor; **o painel vai ser aberto no celular**, às vezes com internet ruim, e biblioteca de dashboard costuma pesar mais que a página inteira; e **rastreador embutido** vem de brinde em várias delas, o que num painel de dado financeiro é inaceitável mesmo sendo dado fictício.

**Custo:** escrevi eixo, grade, tooltip e navegação por teclado na mão, e isso é código que eu tenho que manter. Se um dia o painel precisar de zoom, seleção de período ou cinco tipos de gráfico, a conta vira ao contrário e a biblioteca passa a valer a pena.

---

## 31/07/2026 · Corrigir o nome sujo, mas avisar que corrigiu

**Situação:** cinco linhas da planilha têm espaço sobrando no nome do consultor. Sem tratar, a mesma pessoa aparece duas vezes e os dois totais ficam errados.

**Alternativas:** normalizar em silêncio, mostrar cru para "não mascarar", ou normalizar e avisar.

**Escolhi:** normalizar e avisar, com a contagem escrita na própria seção da página.

Mostrar cru seria fingir rigor: o painel existe para ser lido, e um ranking com a mesma pessoa duas vezes não é honesto, é inútil. Normalizar em silêncio seria pior de outro jeito: o problema está **na origem**, e se o painel esconde, ninguém nunca conserta a planilha.

**Custo:** uma frase a mais numa página que quer ser curta, e ela expõe uma falha do processo interno bem no meio do relatório. É desconfortável de propósito. Relatório que só mostra o que está bonito perde a serventia.

---

## 31/07/2026 · Tabela vira lista no celular, gráfico rola de lado

**Situação:** em 375px, duas das três tabelas passavam de 400px de largura e faziam a página inteira rolar horizontalmente.

**Alternativas:** rolagem lateral em tudo, esconder colunas no celular, ou reempilhar.

**Escolhi:** caminhos diferentes para os dois casos, porque o problema é diferente.

**Tabela vira lista.** Abaixo de 620px cada linha é um bloco com o nome em cima e os valores rotulados embaixo. Nada é escondido e nada rola. Rolar de lado é o pior jeito de ler número: some a primeira coluna, que é justamente o nome da coisa.

**Gráfico rola dentro da própria caixa.** Comprimir doze meses e vinte e quatro barras em 375px deixaria rótulo e eixo ilegíveis. Rolar dentro de um contêiner próprio preserva a leitura sem arrastar a página, e a página avisa que dá para arrastar.

**Custo:** o CSS do modo lista é um bloco de exceção que precisa ser lembrado toda vez que uma coluna nova entrar numa tabela, senão ela aparece sem rótulo no celular. E o gráfico com rolagem tem atrito real: parte do ano fica fora da tela na primeira olhada.

---

## 31/07/2026 · Verificar medindo, não olhando

**Situação:** dava para abrir no navegador, achar que estava bom e seguir.

**Alternativas:** conferir no olho, ou medir.

**Escolhi:** medir. A verificação rodou no navegador e checou número: quantos elementos passam da largura da viewport em 375px (zero), se as linhas empilham, se os rótulos aparecem, o contraste calculado entre texto e fundo nos dois temas, se o tooltip abre no mouse e no teclado.

**Custo:** medida não pega estética. "Nenhum elemento vaza" e "ficou bonito" são coisas diferentes, e a segunda continua sem verificação. Isso está declarado nas limitações do README em vez de escondido.
