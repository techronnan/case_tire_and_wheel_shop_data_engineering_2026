# Databricks notebook source
# DBTITLE 1,Comissoes
dbutils.widgets.text("catalog", "pneustore_dev")
CATALOG = dbutils.widgets.get("catalog")
spark.sql(f"USE CATALOG `{CATALOG}`")
spark.sql("USE SCHEMA `parte1_sql`")

# COMMAND ----------

# Vendedor entra se as 3 maiores comissoes dele ja somam >= 1024 (se as 3 maiores
# nao chegam la, nenhum subconjunto menor chegaria).
rpt_comissoes_vendedores = spark.sql("""
    WITH comissoes_ranqueadas AS (
        SELECT
            vendedor,
            valor,
            ROW_NUMBER() OVER (PARTITION BY vendedor ORDER BY valor DESC) AS rn
        FROM comissoes
    )
    SELECT vendedor
    FROM comissoes_ranqueadas
    WHERE rn <= 3
    GROUP BY vendedor
    HAVING SUM(valor) >= 1024
    ORDER BY vendedor ASC
""")

rpt_comissoes_vendedores.write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG}.parte1_sql.rpt_comissoes_vendedores"
)
print(f"[OK] rpt_comissoes_vendedores -> {rpt_comissoes_vendedores.count()} linhas")
