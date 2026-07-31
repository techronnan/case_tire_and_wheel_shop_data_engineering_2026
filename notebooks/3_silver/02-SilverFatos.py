# Databricks notebook source
# DBTITLE 1,SilverFatos
# MAGIC %run ../0_config/0-Init

# COMMAND ----------

# DBTITLE 1,fato_carrinhos
# Sem tabela de pedidos no dump -> toda linha de tb_carts e tratada como carrinho
# abandonado. Colunas de FK (p_user, p_paymentaddress, ...) chegam como double no
# parquet Hybris -> CAST explicito pra bigint.
fato_carrinhos = (
    spark.table(f"{BRONZE}.tb_carts")
    .select(
        col("pk").cast("bigint").alias("id_carrinho"),
        to_timestamp("createdts", "yyyy-MM-dd HH:mm:ss.SSS").alias("dh_criacao"),
        col("p_totalprice").cast("decimal(18,2)").alias("vl_total"),
        col("p_user").cast("bigint").alias("id_usuario"),
        col("p_paymentaddress").cast("bigint").alias("id_endereco"),
        col("p_paymentinfo").cast("bigint").alias("id_info_pagamento"),
        col("p_paymentmode").cast("bigint").alias("id_forma_pagamento"),
        col("p_site").cast("bigint").alias("id_site"),
    )
    .withColumn("dt_criacao", to_date("dh_criacao"))
    .dropDuplicates(["id_carrinho"])
)
process_data_load(fato_carrinhos, f"{SILVER}.fato_carrinhos", chave="id_carrinho")

# COMMAND ----------

# DBTITLE 1,fato_carrinho_itens
# Sem tabela de produtos no dump -> id_produto e o ID cru de cartentries.p_product.
fato_carrinho_itens = (
    spark.table(f"{BRONZE}.tb_cartentries")
    .select(
        col("pk").cast("bigint").alias("id_item_carrinho"),
        col("p_order").cast("bigint").alias("id_carrinho"),
        col("p_product").cast("bigint").alias("id_produto"),
        col("p_quantity").cast("int").alias("qt_produto"),
        col("p_totalprice").cast("decimal(18,2)").alias("vl_total_item"),
    )
    .dropDuplicates(["id_item_carrinho"])
)
process_data_load(fato_carrinho_itens, f"{SILVER}.fato_carrinho_itens", chave="id_item_carrinho")
