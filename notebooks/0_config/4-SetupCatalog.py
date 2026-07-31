# Databricks notebook source
# DBTITLE 1,SetupCatalog
# Setup unico de infraestrutura Unity Catalog. Roda como primeira task do job,
# antes do landing — nao faz parte da cadeia 0-Init.

dbutils.widgets.text("catalog", "pneus_store")
CATALOG = dbutils.widgets.get("catalog")

print(f"[Setup] Catalog alvo: {CATALOG}")

# COMMAND ----------

# Schemas prefixados com cantustore_ -> catalog pode ja ter landing/bronze/silver/
# gold de outro projeto (ver notebooks/0_config/2-Variables.py)
SCHEMAS = ["cantustore_landing", "cantustore_bronze", "cantustore_silver", "cantustore_gold"]

spark.sql(f"CREATE CATALOG IF NOT EXISTS `{CATALOG}`")

for schema in SCHEMAS:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{CATALOG}`.`{schema}`")

spark.sql(f"CREATE VOLUME IF NOT EXISTS `{CATALOG}`.`cantustore_landing`.`storage_files`")

print(f"✓ Setup concluido | {CATALOG} | schemas: {', '.join(SCHEMAS)}")
