# Decisões do projeto

Registro do **porquê**, não do que foi feito. O código já mostra o que foi feito.

---

## Painel próprio em vez de Power BI ou Looker Studio

**A escolha:** montar a página na mão em vez de publicar um relatório numa ferramenta de BI.

**Por quê:** a pergunta certa não é "qual ferramenta é mais poderosa", é "de que jeito a diretoria recebe melhor a informação". Ferramenta de BI entrega um layout padrão, com o visual dela e o vocabulário dela. Um painel próprio entrega exatamente o recorte que aquela diretoria está acostumada a ler, com o aviso das duas réguas onde ele precisa estar, na linguagem da casa.

Nesse cenário específico, montar rápido um painel personalizado chega mais perto do objetivo do que configurar um relatório em ferramenta tradicional. A mensagem chega mais limpa, e é a mensagem que importa.

Vale registrar que **isso é uma escolha de contexto, não uma regra geral**. Ferramenta de BI ganha fácil quando o dado é atualizado sozinho, quando muita gente precisa fatiar por conta própria, quando existe controle de acesso por área, ou quando não há ninguém para manter código. Aqui nenhuma dessas condições vale: o dado é fechado por período, o público é pequeno e conhecido, e a página tem uma mensagem só.

**O que custa:** manutenção. Cada recorte novo é código, não arrastar campo. Se um dia a diretoria quiser filtrar sozinha por seguradora, por consultor e por trimestre, essa conta vira ao contrário e a ferramenta de BI passa a valer a pena. A hora de trocar é quando começarem a pedir filtro, não antes.

---

## A base continua pronta para qualquer BI, mesmo com painel próprio

**A escolha:** o painel lê os mesmos CSVs em formato longo que qualquer ferramenta leria, e não cria nenhum formato intermediário só dele.

**Por quê:** as duas coisas não competem. O painel próprio é a **apresentação**; a estrutura do dado é a **fundação**. Mantendo a fundação portátil, a mesma base sobe no Power BI, no Looker Studio ou num Postgres sem tratamento, e a escolha da apresentação deixa de ser uma porta trancada.

É o que torna a decisão anterior reversível: trocar de ideia sobre a ferramenta não obriga a refazer o dado.

**O que custa:** nada relevante aqui. O painel poderia ser mais rápido lendo um formato pré-agregado sob medida, mas com esse volume a diferença é imperceptível e não paga o acoplamento.

---

## As duas réguas nunca se subtraem, e isso é regra do código

**A escolha:** nenhuma função de `src/metricas.py` cruza produção comercial com comissão recebida. Cada número carrega o nome da régua que usou, e o aviso no topo da página explica a diferença antes de qualquer valor aparecer.

**Por quê:** a diferença entre vendido e recebido **não é um indicador**. Ela é a distância entre a data da venda e a data do pagamento, e mostrá-la como número faz o leitor achar que é dinheiro faltando. Foi esse erro que a [auditoria](https://github.com/Lucasnevesads/auditoria-comissoes) desmontou. Um painel que o reproduz automatiza o problema em vez de resolvê-lo.

**O que custa:** o painel deixa de responder "quanto falta entrar do que já foi vendido", que é uma pergunta legítima. A resposta certa exigiria cruzar por cronograma de parcelas, não por total. Melhor não responder do que responder errado.

---

## Nenhuma biblioteca no navegador

**A escolha:** SVG, CSS e JavaScript escritos na mão. A página inteira tem 22 KB e não faz nenhuma requisição externa.

**Por quê:** três motivos, em ordem de peso. **CDN é uma porta** que o projeto não controla. **O painel vai ser aberto no celular**, às vezes com internet ruim, e biblioteca de dashboard costuma pesar mais que a página inteira. E **rastreador embutido** vem de brinde em várias delas, o que num painel de dado financeiro é inaceitável mesmo sendo dado fictício.

**O que custa:** eixo, grade, tooltip e navegação por teclado são código para manter. Se o painel precisar de zoom, seleção de período e cinco tipos de gráfico, a conta vira e a biblioteca passa a valer a pena.

---

## Corrigir o nome sujo, mas avisar que corrigiu

**A escolha:** normalizar o espaço sobrando no nome do consultor e escrever na própria página quantas linhas foram normalizadas.

**Por quê:** mostrar cru seria fingir rigor. O painel existe para ser lido, e um ranking com a mesma pessoa duas vezes não é honesto, é inútil. Normalizar em silêncio seria pior de outro jeito: o problema está **na origem**, e se o painel esconde, ninguém nunca conserta a planilha.

**O que custa:** uma frase a mais numa página que quer ser curta, e ela expõe uma falha do processo interno bem no meio do relatório. É desconfortável de propósito. Relatório que só mostra o que está bonito perde a serventia.

---

## Tabela vira lista no celular, gráfico rola de lado

**A escolha:** caminhos diferentes para os dois casos, porque o problema é diferente.

Abaixo de 620px cada linha de tabela vira um bloco, com o nome em cima e os valores rotulados embaixo. Nada é escondido e nada rola. O gráfico, esse sim, rola dentro da própria caixa.

**Por quê:** em 375px duas das três tabelas passavam de 400px e faziam a página inteira rolar de lado, o que some com a primeira coluna, justamente o nome da coisa. Já o gráfico não tem como ser empilhado: comprimir doze meses e vinte e quatro barras em 375px deixaria rótulo e eixo ilegíveis. Rolar dentro de um contêiner próprio preserva a leitura sem arrastar a página.

**O que custa:** o CSS do modo lista é um bloco de exceção que precisa ser lembrado toda vez que uma coluna nova entrar numa tabela, senão ela aparece sem rótulo no celular. E o gráfico com rolagem tem atrito real: parte do ano fica fora da tela na primeira olhada.

---

## Verificar medindo, não olhando

**A escolha:** rodar a verificação no navegador e checar número. Quantos elementos passam da largura da viewport em 375px (zero), se as linhas empilham, se os rótulos aparecem, o contraste calculado entre texto e fundo nos dois temas, se o tooltip abre no mouse e no teclado.

**Por quê:** "abri e achei que estava bom" não é verificação. As duas tabelas que vazavam a tela passariam despercebidas numa olhada rápida em tela grande.

**O que custa:** medida não pega estética. "Nenhum elemento vaza" e "ficou bonito" são coisas diferentes, e a segunda continua sem verificação. Está declarado nas limitações do README em vez de escondido.
