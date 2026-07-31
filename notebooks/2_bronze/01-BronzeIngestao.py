# Databricks notebook source
# DBTITLE 1,BronzeIngestao
# MAGIC %run ../0_config/0-Init

# COMMAND ----------

# Ingestao bruta das 8 tabelas do dump Hybris. Preserva schema/nomes de coluna da
# fonte (so lowercase) -> Delta, upsert por pk_col (idempotente e incremental).
for nome_tabela, fonte in FONTES.items():
    path = f"{LANDING_PATH}/{fonte['file']}"

    if fonte["format"] == "parquet":
        df = spark.read.parquet(path)
    else:
        df = (
            spark.read.option("header", "true")
            .option("delimiter", fonte["sep"])
            .option("quote", '"')
            .csv(path)
        )

    df_bronze = (
        df.select([col(c).alias(c.lower()) for c in df.columns])
        .withColumn("dh_carga_bronze", current_timestamp())
        .withColumn("nm_arquivo_origem", lit(fonte["file"]))
    )

    process_data_load(df_bronze, f"{BRONZE}.{nome_tabela}", chave=fonte["pk_col"])
