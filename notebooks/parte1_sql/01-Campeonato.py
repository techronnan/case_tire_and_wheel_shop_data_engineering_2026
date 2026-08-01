# Databricks notebook source
# DBTITLE 1,Campeonato
dbutils.widgets.text("catalog", "pneustore_dev")
CATALOG = dbutils.widgets.get("catalog")
spark.sql(f"USE CATALOG `{CATALOG}`")
spark.sql("USE SCHEMA `parte1_sql`")

# COMMAND ----------

# Pontos por time (vitoria=3, empate=1, derrota=0). LEFT JOIN a partir de `times`
# pra time sem partida entrar com 0.
rpt_campeonato = spark.sql("""
    WITH resultados AS (
        SELECT mandante_time AS time_id,
            CASE WHEN mandante_gols > visitante_gols THEN 3
                 WHEN mandante_gols = visitante_gols THEN 1 ELSE 0 END AS pontos
        FROM jogos
        UNION ALL
        SELECT visitante_time AS time_id,
            CASE WHEN visitante_gols > mandante_gols THEN 3
                 WHEN visitante_gols = mandante_gols THEN 1 ELSE 0 END AS pontos
        FROM jogos
    )
    SELECT
        t.time_id,
        t.time_nome,
        COALESCE(SUM(r.pontos), 0) AS num_pontos
    FROM times t
    LEFT JOIN resultados r ON r.time_id = t.time_id
    GROUP BY t.time_id, t.time_nome
    ORDER BY num_pontos DESC, t.time_id ASC
""")

rpt_campeonato.write.format("delta").mode("overwrite").saveAsTable(f"{CATALOG}.parte1_sql.rpt_campeonato")
print(f"[OK] rpt_campeonato -> {rpt_campeonato.count()} linhas")
