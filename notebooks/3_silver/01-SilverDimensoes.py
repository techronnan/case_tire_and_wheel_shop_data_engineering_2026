# Databricks notebook source
# DBTITLE 1,SilverDimensoes
# MAGIC %run ../0_config/0-Init

# COMMAND ----------

# DBTITLE 1,dim_regioes
dim_regioes = (
    spark.table(f"{BRONZE}.tb_regions")
    .select(
        col("pk").cast("bigint").alias("id_regiao"),
        col("p_isocodeshort").alias("sg_uf"),
        col("p_isocode").alias("cd_isocode"),
        (col("p_active") == lit("1")).alias("fl_ativo"),
    )
    .dropDuplicates(["id_regiao"])
)
process_data_load(dim_regioes, f"{SILVER}.dim_regioes", chave="id_regiao")

# COMMAND ----------

# DBTITLE 1,dim_formas_pagamento
dim_formas_pagamento = (
    spark.table(f"{BRONZE}.tb_paymentmodes")
    .select(
        col("pk").cast("bigint").alias("id_forma_pagamento"),
        col("p_code").alias("cd_forma_pagamento"),
        (col("p_active") == lit("1")).alias("fl_ativo"),
    )
    .dropDuplicates(["id_forma_pagamento"])
)
process_data_load(dim_formas_pagamento, f"{SILVER}.dim_formas_pagamento", chave="id_forma_pagamento")

# COMMAND ----------

# DBTITLE 1,dim_sites
dim_sites = (
    spark.table(f"{BRONZE}.tb_cmssitelp")
    .select(
        col("itempk").cast("bigint").alias("id_site"),
        col("p_name").alias("nm_site"),
    )
    .dropDuplicates(["id_site"])
)
process_data_load(dim_sites, f"{SILVER}.dim_sites", chave="id_site")

# COMMAND ----------

# DBTITLE 1,dim_pagamento_parcelas
dim_pagamento_parcelas = (
    spark.table(f"{BRONZE}.tb_paymentinfos")
    .select(
        col("pk").cast("bigint").alias("id_info_pagamento"),
        col("p_installments").cast("int").alias("qt_parcelas"),
    )
    .dropDuplicates(["id_info_pagamento"])
)
process_data_load(dim_pagamento_parcelas, f"{SILVER}.dim_pagamento_parcelas", chave="id_info_pagamento")

# COMMAND ----------

# DBTITLE 1,dim_usuarios
# Muitas linhas de tb_users tem so pk preenchido (registros tecnicos do Hybris) -
# mantidas mesmo sem p_uid, nunca descartadas.
dim_usuarios = (
    spark.table(f"{BRONZE}.tb_users")
    .select(
        col("pk").cast("bigint").alias("id_usuario"),
        col("p_uid").alias("cd_uid"),
    )
    .dropDuplicates(["id_usuario"])
)
process_data_load(dim_usuarios, f"{SILVER}.dim_usuarios", chave="id_usuario")

# COMMAND ----------

# DBTITLE 1,dim_enderecos
# sg_uf denormalizada aqui (broadcast join com dim_regioes, ja gravada acima) pra
# Q5 (estados) nao precisar de mais um join na Gold.
enderecos = spark.table(f"{BRONZE}.tb_addresses").select(
    col("pk").cast("bigint").alias("id_endereco"),
    col("p_region").cast("bigint").alias("id_regiao"),
    col("p_postalcode").alias("cd_cep"),
    col("p_town").alias("nm_cidade"),
    col("p_district").alias("nm_bairro"),
)

dim_enderecos = (
    enderecos.join(broadcast(dim_regioes.select("id_regiao", "sg_uf")), on="id_regiao", how="left")
    .select("id_endereco", "id_regiao", "sg_uf", "cd_cep", "nm_cidade", "nm_bairro")
    .dropDuplicates(["id_endereco"])
)
process_data_load(dim_enderecos, f"{SILVER}.dim_enderecos", chave="id_endereco")
