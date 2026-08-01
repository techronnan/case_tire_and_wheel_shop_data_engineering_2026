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


def check_quality(nome_tabela: str, chave: str) -> list:
    """Checa linhas>0, chave sem nulo e sem duplicata. Retorna lista de falhas (vazia = ok)."""
    df = spark.table(nome_tabela)
    total = df.count()
    falhas = []
    if total == 0:
        return [f"{nome_tabela}: 0 linhas"]
    nulos = df.filter(col(chave).isNull()).count()
    if nulos > 0:
        falhas.append(f"{nome_tabela}: {nulos} linha(s) com {chave} nulo")
    distintos = df.select(chave).distinct().count()
    if distintos != total:
        falhas.append(f"{nome_tabela}: {chave} duplicado ({total} linhas, {distintos} distintos)")
    return falhas


print("[Functions] carregadas | process_data_load, check_quality")
