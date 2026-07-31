# Databricks notebook source
spark.conf.set("spark.sql.session.timeZone", "America/Sao_Paulo")

print(f"[Init] Spark {spark.version} | TZ: America/Sao_Paulo")

# COMMAND ----------

# MAGIC %run ./1-Libs

# COMMAND ----------

# MAGIC %run ./2-Variables

# COMMAND ----------

# MAGIC %run ./3-Functions

# COMMAND ----------

print(f"✓ Config carregado | {PIPELINE_NAME} | Catalog: {CATALOG}")
