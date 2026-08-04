# Databricks notebook source
# DBTITLE 1,GoldRelatorios
# MAGIC %run ../0_config/0-Init

# COMMAND ----------

fato_carrinhos = spark.table(f"{SILVER}.fato_carrinhos")
fato_itens = spark.table(f"{SILVER}.fato_carrinho_itens")

# COMMAND ----------

# DBTITLE 1,Relatorio produto x mes
# Grao e o item de carrinho -> usa vl_total_item (valor nao faturado e a fatia do
# produto dentro do carrinho, nao o total do carrinho).
itens_com_mes = fato_itens.join(
    fato_carrinhos.select("id_carrinho", "dt_criacao"), "id_carrinho"
).withColumn("dt_mes", trunc("dt_criacao", "month"))

rpt_mensal_produto = (
    itens_com_mes.groupBy("id_produto", "dt_mes")
    .agg(
        countDistinct("id_carrinho").alias("qt_carrinhos_abandonados"),
        _sum("qt_produto").alias("qt_itens_abandonados"),
        _sum("vl_total_item").alias("vl_nao_faturado"),
    )
    .orderBy("dt_mes", "id_produto")
)
display(rpt_mensal_produto.limit(20))
process_data_load(rpt_mensal_produto, f"{GOLD}.rpt_mensal_produto")

# COMMAND ----------

# DBTITLE 1,Relatorio diario
# Grao e o carrinho -> usa vl_total do cabecalho.
carrinhos_por_dia = fato_carrinhos.groupBy("dt_criacao").agg(
    countDistinct("id_carrinho").alias("qt_carrinhos_abandonados"),
    _sum("vl_total").alias("vl_nao_faturado"),
)

itens_por_dia = itens_com_mes.groupBy("dt_criacao").agg(_sum("qt_produto").alias("qt_itens_abandonados"))

rpt_diario = (
    carrinhos_por_dia.join(itens_por_dia, on="dt_criacao", how="left")
    .select("dt_criacao", "qt_carrinhos_abandonados", "qt_itens_abandonados", "vl_nao_faturado")
    .orderBy("dt_criacao")
)
display(rpt_diario.limit(20))
process_data_load(rpt_diario, f"{GOLD}.rpt_diario")
