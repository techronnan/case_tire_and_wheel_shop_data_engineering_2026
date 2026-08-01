# Databricks notebook source
# DBTITLE 1,Parte1SqlSetup
# Cria o schema e as 4 tabelas de exemplo da Parte 1 (SQL) do case, com o dado do
# proprio enunciado. Roda toda vez (CREATE OR REPLACE / INSERT OVERWRITE) - e
# dado estatico de exercicio, nao tem carga incremental real.
dbutils.widgets.text("catalog", "pneustore_dev")
CATALOG = dbutils.widgets.get("catalog")
SCHEMA = "parte1_sql"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{CATALOG}`.`{SCHEMA}`")
spark.sql(f"USE CATALOG `{CATALOG}`")
spark.sql(f"USE SCHEMA `{SCHEMA}`")

# COMMAND ----------

# DBTITLE 1,times + jogos (1.1 Campeonato)
spark.sql("""
    CREATE OR REPLACE TABLE times (
        time_id INTEGER NOT NULL
        ,time_nome STRING NOT NULL
    )
""")
spark.sql("""
    INSERT OVERWRITE times VALUES
        (10, 'Financeiro'), (20, 'Marketing'), (30, 'Logística'), (40, 'TI'), (50, 'Dados')
""")

spark.sql("""
    CREATE OR REPLACE TABLE jogos (
        jogo_id INTEGER NOT NULL
        , mandante_time INTEGER NOT NULL
        , visitante_time INTEGER NOT NULL
        , mandante_gols INTEGER NOT NULL
        , visitante_gols INTEGER NOT NULL
    )
""")
spark.sql("""
    INSERT OVERWRITE jogos VALUES
        (1, 30, 20, 1, 0), (2, 10, 20, 1, 2), (3, 20, 50, 2, 2), (4, 10, 30, 1, 0), (5, 30, 50, 0, 1)
""")

# COMMAND ----------

# DBTITLE 1,comissoes (1.2 Comissoes)
spark.sql("""
    CREATE OR REPLACE TABLE comissoes (
        comprador STRING NOT NULL
        ,vendedor STRING NOT NULL
        ,dataPgto DATE NOT NULL
        ,valor DOUBLE NOT NULL
    )
""")
spark.sql("""
    INSERT OVERWRITE comissoes VALUES
        ('Leonardo', 'Bruno',   DATE'2000-01-01', 200.00),
        ('Leonardo', 'Matheus', DATE'2003-09-27', 1024.00),
        ('Leonardo', 'Lucas',   DATE'2006-06-26', 512.00),
        ('Marcos',   'Lucas',   DATE'2020-12-17', 100.00),
        ('Marcos',   'Lucas',   DATE'2002-03-22', 10.00),
        ('Cinthia',  'Lucas',   DATE'2021-03-20', 500.00),
        ('Mateus',   'Bruno',   DATE'2007-06-02', 400.00),
        ('Mateus',   'Bruno',   DATE'2006-06-26', 400.00),
        ('Mateus',   'Bruno',   DATE'2015-06-26', 200.00)
""")

# COMMAND ----------

# DBTITLE 1,colaboradores (1.3 Organizacao Empresarial)
spark.sql("""
    CREATE OR REPLACE TABLE colaboradores (
        id INTEGER NOT NULL
        , nome STRING NOT NULL
        , salario INTEGER NOT NULL
        , lider_id INTEGER
    )
""")
spark.sql("""
    INSERT OVERWRITE colaboradores VALUES
        (40, 'Helen', 1500, 50),
        (50, 'Bruno', 3000, 10),
        (10, 'Leonardo', 4500, 20),
        (20, 'Marcos', 10000, NULL),
        (70, 'Mateus', 1500, 10),
        (60, 'Cinthia', 2000, 70),
        (30, 'Wilian', 1501, 50)
""")

print(f"✓ Setup Parte 1 SQL concluido | {CATALOG}.{SCHEMA} | times, jogos, comissoes, colaboradores")
