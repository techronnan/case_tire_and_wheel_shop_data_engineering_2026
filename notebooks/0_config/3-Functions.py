# Databricks notebook source
def process_data_load(df: DataFrame, nome_tabela: str, chave: str = None) -> int:
    """Grava tabela Delta. Com `chave`, faz upsert (MERGE) por PK - idempotente e
    incremental em reexecucoes. Sem `chave` (tabelas Gold agregadas), overwrite."""
    if chave and spark.catalog.tableExists(nome_tabela):
        df.createOrReplaceTempView("_merge_source")
        spark.sql(f"""
            MERGE INTO {nome_tabela} AS target
            USING _merge_source AS source
            ON target.{chave} = source.{chave}
            WHEN MATCHED THEN UPDATE SET *
            WHEN NOT MATCHED THEN INSERT *
        """)
    else:
        df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(nome_tabela)

    linhas = spark.table(nome_tabela).count()
    print(f"  [OK] {nome_tabela} -> {linhas:,} linhas")
    return linhas


print("[Functions] carregadas | process_data_load")
