# Case — Engenheiro de Dados

Entrega de um teste técnico para vaga de Engenheiro de Dados, dividido em duas partes.

A primeira é SQL: um ranking de campeonato por pontos, uma consulta sobre comissões
de vendedores (soma de subconjuntos de transferências) e uma consulta recursiva de
hierarquia de funcionários (achar o chefe indireto mais próximo que ganha pelo menos
o dobro do salário). Respostas em [sql/](sql/).

A segunda parte é uma análise de carrinho abandonado num e-commerce (dataset SAP
Hybris/Commerce Cloud, ~33M linhas em 8 tabelas). As principais perguntas que o
pipeline responde:

- quais produtos mais tiveram carrinhos abandonados
- quais duplas de produtos mais aparecem juntas nesses carrinhos
- quais produtos tiveram aumento de abandono mês a mês
- quais produtos são novos e quantos carrinhos tiveram no primeiro mês
- quais estados concentram mais abandonos

Além disso, dois relatórios de acompanhamento (produto × mês e por data, com
quantidade de carrinhos, itens e valor não faturado) e um export `.txt` com os 50
carrinhos de maior valor.

Todo esse pipeline roda em Databricks: ingestão (Landing → Bronze), tratamento e
tipagem (Silver) e as tabelas de resposta (Gold), orquestrado como um Job via
Databricks Asset Bundles.

<!-- imagem: arquitetura do pipeline -->

<!-- imagem: workflow rodando no Databricks -->

<!-- imagem: resultado / tabelas Gold -->

## Conteúdo

- `sql/` — respostas da Parte 1
- `notebooks/` — pipeline da Parte 2 (Landing, Bronze, Silver, Gold)
- `databricks.yml` + `resources/jobs/` — Asset Bundle
