# Databricks notebook source
# DBTITLE 1,GoldExportTop50
# MAGIC %run ../0_config/0-Init

# COMMAND ----------

spark.sql(f"CREATE VOLUME IF NOT EXISTS `{CATALOG}`.`{GOLD_SCHEMA}`.`exports`")

fato_carrinhos = spark.table(f"{SILVER}.fato_carrinhos")
fato_itens = spark.table(f"{SILVER}.fato_carrinho_itens")
dim_usuarios = spark.table(f"{SILVER}.dim_usuarios")
dim_formas_pagamento = spark.table(f"{SILVER}.dim_formas_pagamento")
dim_pagamento_parcelas = spark.table(f"{SILVER}.dim_pagamento_parcelas")
dim_sites = spark.table(f"{SILVER}.dim_sites")
dim_enderecos = spark.table(f"{SILVER}.dim_enderecos")

# COMMAND ----------

itens_agregados = fato_itens.groupBy("id_carrinho").agg(
    _sum("qt_produto").alias("qt_total_itens"),
    count("*").alias("qt_linhas_item"),
)

top50 = (
    fato_carrinhos.join(dim_usuarios, "id_usuario", "left")
    .join(dim_formas_pagamento, "id_forma_pagamento", "left")
    .join(dim_pagamento_parcelas, "id_info_pagamento", "left")
    .join(dim_sites, "id_site", "left")
    .join(dim_enderecos, "id_endereco", "left")
    .join(itens_agregados, "id_carrinho", "left")
    .orderBy(col("vl_total").desc())
    .limit(50)
    .select(
        col("id_carrinho").alias("pk"),
        date_format("dh_criacao", "yyyy-MM-dd HH:mm:ss").alias("created_ts"),
        col("vl_total"),
        col("cd_uid"),
        col("cd_forma_pagamento"),
        col("qt_parcelas"),
        col("nm_site"),
        col("cd_cep"),
        col("qt_total_itens"),
        col("qt_linhas_item"),
    )
)

# collect() seguro aqui: so 50 carrinhos, resultado ja pequeno
cabecalhos = top50.orderBy(col("vl_total").desc()).collect()
ids_top50 = [row["pk"] for row in cabecalhos]

itens_top50 = (
    fato_itens.filter(col("id_carrinho").isin(ids_top50))
    .select("id_carrinho", "id_produto", "qt_produto", "vl_total_item")
    .collect()
)

# COMMAND ----------


def fmt(valor):
    return "" if valor is None else str(valor)


itens_por_carrinho = {}
for item in itens_top50:
    itens_por_carrinho.setdefault(item["id_carrinho"], []).append(item)

# Layout hierarquico exato da prova: 1 linha de cabecalho (sem | final) + N linhas
# de item (com | final), uma por cartentries daquele carrinho.
linhas = []
for cabecalho in cabecalhos:
    linhas.append(
        "|".join(
            [
                fmt(cabecalho["pk"]),
                fmt(cabecalho["created_ts"]),
                fmt(cabecalho["vl_total"]),
                fmt(cabecalho["cd_uid"]),
                fmt(cabecalho["cd_forma_pagamento"]),
                fmt(cabecalho["qt_parcelas"]),
                fmt(cabecalho["nm_site"]),
                fmt(cabecalho["cd_cep"]),
                fmt(cabecalho["qt_total_itens"]),
                fmt(cabecalho["qt_linhas_item"]),
            ]
        )
    )
    for item in itens_por_carrinho.get(cabecalho["pk"], []):
        linhas.append(f"{fmt(item['id_produto'])}|{fmt(item['qt_produto'])}|{fmt(item['vl_total_item'])}|")

# COMMAND ----------

export_path = f"/Volumes/{CATALOG}/{GOLD_SCHEMA}/exports/top50_carrinhos_abandonados.txt"

with open(export_path, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas) + "\n")

print(f"✓ Export gravado em {export_path} | {len(cabecalhos)} carrinhos | {len(linhas)} linhas")
