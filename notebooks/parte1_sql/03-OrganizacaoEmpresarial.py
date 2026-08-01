# Databricks notebook source
# DBTITLE 1,OrganizacaoEmpresarial
dbutils.widgets.text("catalog", "pneustore_dev")
CATALOG = dbutils.widgets.get("catalog")
spark.sql(f"USE CATALOG `{CATALOG}`")
spark.sql("USE SCHEMA `parte1_sql`")

# COMMAND ----------

# O chefe indireto "mais baixo na hierarquia" que ganha o dobro = o primeiro chefe
# subindo a cadeia (chefe direto, depois chefe do chefe...) que bate a condicao de
# salario - porque quem esta mais perto do funcionario sempre tem mais chefes
# indiretos acima de si do que quem esta mais longe.
rpt_organizacao_chefes = spark.sql("""
    WITH RECURSIVE hierarquia AS (
        SELECT
            c.id AS funcionario_id,
            c.salario AS salario_funcionario,
            c.lider_id AS chefe_id,
            1 AS nivel
        FROM colaboradores c
        WHERE c.lider_id IS NOT NULL

        UNION ALL

        SELECT
            h.funcionario_id,
            h.salario_funcionario,
            chefe_atual.lider_id AS chefe_id,
            h.nivel + 1 AS nivel
        FROM hierarquia h
        JOIN colaboradores chefe_atual ON chefe_atual.id = h.chefe_id
        WHERE chefe_atual.lider_id IS NOT NULL
    ),

    candidatos AS (
        SELECT h.funcionario_id, h.chefe_id, h.nivel
        FROM hierarquia h
        JOIN colaboradores chefe ON chefe.id = h.chefe_id
        WHERE chefe.salario >= 2 * h.salario_funcionario
    ),

    melhor_chefe AS (
        SELECT
            funcionario_id,
            chefe_id,
            ROW_NUMBER() OVER (PARTITION BY funcionario_id ORDER BY nivel ASC) AS rn
        FROM candidatos
    )

    SELECT
        c.id AS id_funcionario,
        mc.chefe_id AS id_chefe
    FROM colaboradores c
    LEFT JOIN melhor_chefe mc ON mc.funcionario_id = c.id AND mc.rn = 1
    ORDER BY c.id ASC
""")

rpt_organizacao_chefes.write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG}.parte1_sql.rpt_organizacao_chefes"
)
print(f"[OK] rpt_organizacao_chefes -> {rpt_organizacao_chefes.count()} linhas")
