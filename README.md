# Case CantuStore — Engenheiro de Dados

Teste técnico da CantuStore (plataforma de tecnologia e logística para pneus).
Enunciado original em [artefatos_do_case/ProvaDados.pdf](artefatos_do_case/ProvaDados.pdf).

- **Parte 1 (SQL)** — [sql/](sql/): campeonato, comissões, organização empresarial.
- **Parte 2 (carrinho abandonado)** — pipeline Databricks (PySpark) em `notebooks/`,
  arquitetura Medallion (Landing → Bronze → Silver → Gold), deployado via
  Databricks Asset Bundles no Free Edition.

## Estrutura

```
notebooks/
├── 0_config/      # catalog, paths, mapeamento das fontes, funções compartilhadas
├── 1_landing/      # baixa os arquivos do Google Drive pro Volume
├── 2_bronze/       # ingestão bruta das 8 tabelas
├── 3_silver/       # tipagem, conformidade
└── 4_gold/         # respostas das 5 perguntas + 2 relatórios + export top-50
sql/                 # Parte 1 da prova
databricks.yml + resources/jobs/   # Asset Bundle
```

## Dados

O dump (SAP Hybris/Commerce Cloud, 8 tabelas) é grande demais pra caber no git
(`tb_carts.zip` sozinho tem 698MB) — fica numa pasta do Google Drive, e o notebook
de Landing baixa tudo pra um Volume Unity Catalog antes da ingestão Bronze.

## Rodar

```bash
databricks auth login --host <seu-workspace-free-edition>
databricks bundle deploy -t dev
databricks bundle run wf_cantustore_carrinho_abandonado -t dev
```

Catalog default: `pneus_store` (schemas `cantustore_landing/bronze/silver/gold`,
ajustável via variável `catalog` em `databricks.yml`).

## Premissas

O dump não tem tabela de pedidos nem de produtos:
- carrinho abandonado = toda linha de `tb_carts`
- produto = ID cru de `cartentries.p_product`, sem nome/categoria
- "mês de lançamento" de um produto = primeiro mês em que ele aparece nos carrinhos
