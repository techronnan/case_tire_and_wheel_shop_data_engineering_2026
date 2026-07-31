# Databricks notebook source
# DBTITLE 1,GoldPerguntasNegocio
# MAGIC %run ../0_config/0-Init

# COMMAND ----------

fato_carrinhos = spark.table(f"{SILVER}.fato_carrinhos")
fato_itens = spark.table(f"{SILVER}.fato_carrinho_itens")
dim_enderecos = spark.table(f"{SILVER}.dim_enderecos")

itens_com_data = fato_itens.join(
    fato_carrinhos.select("id_carrinho", "dt_criacao"), "id_carrinho"
).withColumn("dt_mes", trunc("dt_criacao", "month"))

# COMMAND ----------

# DBTITLE 1,Q1 - produtos com mais carrinhos abandonados
rpt_produtos_mais_abandonados = (
    itens_com_data.groupBy("id_produto")
    .agg(
        countDistinct("id_carrinho").alias("qt_carrinhos_abandonados"),
        _sum("qt_produto").alias("qt_itens_abandonados"),
    )
    .orderBy(col("qt_carrinhos_abandonados").desc())
)
process_data_load(rpt_produtos_mais_abandonados, f"{GOLD}.rpt_produtos_mais_abandonados")

# COMMAND ----------

# DBTITLE 1,Q2 - duplas de produtos que mais aparecem juntas
itens_a = itens_com_data.select("id_carrinho", col("id_produto").alias("id_produto_a"))
itens_b = itens_com_data.select("id_carrinho", col("id_produto").alias("id_produto_b"))

rpt_duplas_produtos_abandonados = (
    itens_a.join(itens_b, on="id_carrinho")
    .filter(col("id_produto_a") < col("id_produto_b"))  # evita par duplicado/auto-par
    .groupBy("id_produto_a", "id_produto_b")
    .agg(countDistinct("id_carrinho").alias("qt_carrinhos_abandonados"))
    .orderBy(col("qt_carrinhos_abandonados").desc())
)
process_data_load(rpt_duplas_produtos_abandonados, f"{GOLD}.rpt_duplas_produtos_abandonados")

# COMMAND ----------

# DBTITLE 1,Q3 - produtos com aumento de abandono (mes a mes)
por_produto_mes = itens_com_data.groupBy("id_produto", "dt_mes").agg(
    countDistinct("id_carrinho").alias("qt_carrinhos_abandonados")
)

janela_produto = Window.partitionBy("id_produto").orderBy("dt_mes")

tendencia = por_produto_mes.withColumn(
    "qt_carrinhos_mes_anterior", lag("qt_carrinhos_abandonados").over(janela_produto)
).withColumn("var_qt_carrinhos", col("qt_carrinhos_abandonados") - col("qt_carrinhos_mes_anterior"))

ultimo_mes = itens_com_data.agg(_max("dt_mes")).first()[0]

rpt_produtos_aumento_abandono = (
    tendencia.filter((col("dt_mes") == lit(ultimo_mes)) & (col("var_qt_carrinhos") > 0))
    .orderBy(col("var_qt_carrinhos").desc())
)
process_data_load(rpt_produtos_aumento_abandono, f"{GOLD}.rpt_produtos_aumento_abandono")

# COMMAND ----------

# DBTITLE 1,Q4 - produtos novos e volume no primeiro mes
# "Produto novo"/"mes de lancamento" = primeiro mes em que o produto aparece no
# dataset de carrinhos (sem data de cadastro de catalogo nos dados fornecidos).
primeiro_mes_produto = itens_com_data.groupBy("id_produto").agg(_min("dt_mes").alias("dt_mes_lancamento"))

rpt_produtos_novos_ultimo_mes = (
    itens_com_data.join(primeiro_mes_produto, on="id_produto")
    .filter((col("dt_mes") == col("dt_mes_lancamento")) & (col("dt_mes_lancamento") == lit(ultimo_mes)))
    .groupBy("id_produto", "dt_mes_lancamento")
    .agg(countDistinct("id_carrinho").alias("qt_carrinhos_primeiro_mes"))
    .orderBy(col("qt_carrinhos_primeiro_mes").desc())
)
process_data_load(rpt_produtos_novos_ultimo_mes, f"{GOLD}.rpt_produtos_novos_ultimo_mes")

# COMMAND ----------

# DBTITLE 1,Q5 - estados com mais abandonos
rpt_estados_mais_abandonos = (
    fato_carrinhos.join(dim_enderecos, on="id_endereco", how="left")
    .groupBy("sg_uf")
    .agg(countDistinct("id_carrinho").alias("qt_carrinhos_abandonados"))
    .orderBy(col("qt_carrinhos_abandonados").desc())
)
process_data_load(rpt_estados_mais_abandonos, f"{GOLD}.rpt_estados_mais_abandonos")
