# Prova Equipe de Dados — CantuStore

Somos a CantuStore: plataforma de tecnologia e logística que viabiliza soluções completas em pneus,
guiando quem compra e apoiando quem vende.

## Parte 1 - SQL

### 1.1 Campeonato

```sql
CREATE TABLE times(
    time_id INTEGER NOT NULL
    ,time_nome VARCHAR NOT NULL
    UNIQUE(time_id)
)
```

| time_id | time_nome |
|---|---|
| 10 | Financeiro |
| 20 | Marketing |
| 30 | Logística |
| 40 | TI |
| 50 | Dados |

```sql
CREATE TABLE jogos (
    jogo_id INTEGER NOT NULL
    , mandante_time INTEGER NOT NULL
    , visitante_time INTEGER NOT NULL
    , mandante_gols INTEGER NOT NULL
    , visitante_gols INTEGER NOT NULL
    UNIQUE(jogo_id)
)
```

| jogo_id | mandante_time | visitante_time | mandante_gols | visitante_gols |
|---|---|---|---|---|
| 1 | 30 | 20 | 1 | 0 |
| 2 | 10 | 20 | 1 | 2 |
| 3 | 20 | 50 | 2 | 2 |
| 4 | 10 | 30 | 1 | 0 |
| 5 | 30 | 50 | 0 | 1 |

Calcule o número total de pontos que cada equipe marcou após todas as partidas:

- vitória (mais gols que o adversário) = 3 pontos;
- empate (mesmo número de gols) = 1 ponto;
- derrota (menos gols que o adversário) = 0 pontos.

Escreva uma consulta que retorne uma classificação de todas as equipes (`time_id`) descritas na
tabela `times`, com nome e número de pontos (`num_pontos`), ordenada por `num_pontos` desc e,
em caso de empate, por `time_id`.

### 1.2 Comissões

```sql
CREATE TABLE comissoes (
    comprador VARCHAR NOT NULL
    ,vendedor VARCHAR NOT NULL
    ,dataPgto DATE NOT NULL
    ,valor FLOAT NOT NULL
)
```

Escreva uma query que retorne a lista de vendedores que têm recebido até 1024 reais em até três
transferências — ou seja, o vendedor é listado se existirem três ou menos comissões cuja soma dos
valores recebidos não seja inferior a 1024 reais. Pode haver mais de três comissões para o mesmo
vendedor, desde que três ou menos delas totalizem pelo menos 1024 reais. Ordenar por nome do
vendedor (asc). Comprador é sempre diferente do vendedor em cada linha.

Exemplo:

| Comprador | Vendedor | Data | Valor |
|---|---|---|---|
| Leonardo | Bruno | 01/01/2000 | 200,00 |
| Leonardo | Matheus | 27/09/2003 | 1.024,00 |
| Leonardo | Lucas | 26/06/2006 | 512,00 |
| Marcos | Lucas | 17/12/2020 | 100,00 |
| Marcos | Lucas | 22/03/2002 | 10,00 |
| Cinthia | Lucas | 20/03/2021 | 500,00 |
| Mateus | Bruno | 02/06/2007 | 400,00 |
| Mateus | Bruno | 26/06/2006 | 400,00 |
| Mateus | Bruno | 26/06/2015 | 200,00 |

- Lucas é listado: 512 + 100 + 500 = 1112 em três vendas.
- Matheus é listado: 1024 em uma única transferência.
- Bruno **não** é listado: recebeu 1200 em quatro vendas, mas nenhum subconjunto de três chega a 1024.

### 1.3 Organização Empresarial

Empresa em que cada empregado recebe um salário e tem no máximo um chefe direto. O funcionário
A é chefe indireto do funcionário B se A é chefe direto de B, ou A é chefe indireto do chefe direto de
B (chefe direto de B, chefe direto do chefe direto de B, etc).

Exemplo de hierarquia (`A -> B` = B é chefe direto de A):

```
Leonardo -> Bruno
Bruno -> Cinthia
Cinthia -> Mateus
Pedro -> Cinthia
```

Os chefes indiretos de Leonardo são Bruno, Cinthia e Mateus (Pedro não é).

Um funcionário A é "mais baixo na hierarquia" que B se A tem mais chefes indiretos que B. No exemplo,
Leonardo (três chefes indiretos) é mais baixo na hierarquia que Pedro (dois chefes indiretos).

```sql
CREATE TABLE colaboradores (
    id INTEGER NOT NULL
    , nome VARCHAR NOT NULL
    , salario INTEGER NOT NULL
    , lider_id INTEGER NOT NULL
    UNIQUE(id)
)
```

`lider_id` é o chefe direto (NULL se não tiver). Sem referências cíclicas. Salário sempre >= 0.

Para cada funcionário, encontrar o chefe indireto de classificação **mais baixa** na hierarquia que
ganha pelo menos o dobro do funcionário. Retornar (id do funcionário, id do chefe), ordenado por id
do funcionário, todos os funcionários presentes, NULL quando nenhum chefe indireto cumpre a
condição.

Exemplo:

| Id | Nome | Salário | Lider_Id |
|---|---|---|---|
| 40 | Helen | 1500 | 50 |
| 50 | Bruno | 3000 | 10 |
| 10 | Leonardo | 4500 | 20 |
| 20 | Marcos | 10000 | NULL |
| 70 | Mateus | 1500 | 10 |
| 60 | Cinthia | 2000 | 70 |
| 30 | Wilian | 1501 | 50 |

## Parte 2 - Análise de Dados

Um dos problemas mais clássicos do e-commerce é o carrinho abandonado: cliente seleciona produtos
mas não finaliza a compra. Estratégias de recuperação incluem remarketing, frete flexível e checkout
melhor. Analisar esses eventos ajuda a entender por que os clientes desistem.

Dataset SAP Hybris/Commerce Cloud com ~33M linhas em 8 tabelas relacionadas:
`tb_carts`, `tb_cartentries`, `tb_users`, `tb_addresses`, `tb_regions`, `tb_paymentmodes`,
`tb_paymentinfos`, `tb_cmssitelp`. `tb_carts` é a tabela central, referenciando usuário, endereço de
pagamento, forma de pagamento, info de pagamento e site; `tb_cartentries` referencia o carrinho
(itens do carrinho); `tb_addresses` referencia `tb_regions`.

> O link de download do dump bruto foi fornecido separadamente pela CantuStore (pasta
> compartilhada) e não é reproduzido aqui.

Perguntas a responder:

- Quais os produtos que mais tiveram carrinhos abandonados?
- Quais as duplas de produtos em conjunto que mais tiveram carrinhos abandonados?
- Quais produtos tiveram um aumento de abandono?
- Quais os produtos novos e a quantidade de carrinhos no seu primeiro mês de lançamento?
- Quais estados tiveram mais abandonos?

Além disso:

- Relatório dos produtos, mês a mês: quantidade de carrinhos abandonados, quantidade de itens
  abandonados e valor não faturado.
- Relatório por data: quantidade de carrinhos abandonados, quantidade de itens abandonados e
  valor não faturado.

Exportar um `.txt` com os 50 carrinhos de maior `carts.p_totalprice`, no layout:

```
carts.PK|carts.createdTS|carts.p_totalprice|user.p_uid|paymentmodes.p_code|paymentinfos.p_installments|cmssitelp.p_name|addresses.p_postalcode|sum(cartentries.p_quantity)|count(cartentries.PK)
cartentries.p_product|cartentries.p_quantity|cartentries.p_totalprice|
cartentries.p_product|cartentries.p_quantity|cartentries.p_totalprice|
...
```

Uma linha de cabeçalho por carrinho, seguida de uma linha por item do carrinho (`cartentries`).

Python + qualquer plataforma de notebooks é aceito; usar Databricks e PySpark é um diferencial.
