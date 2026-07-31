# Databricks notebook source
dbutils.widgets.text("catalog", "pneus_store")
CATALOG = dbutils.widgets.get("catalog")

LANDING_SCHEMA = "landing"
BRONZE_SCHEMA = "bronze"
SILVER_SCHEMA = "silver"
GOLD_SCHEMA = "gold"

BRONZE = f"{CATALOG}.{BRONZE_SCHEMA}"
SILVER = f"{CATALOG}.{SILVER_SCHEMA}"
GOLD = f"{CATALOG}.{GOLD_SCHEMA}"

# COMMAND ----------

# DBTITLE 1,Paths - landing
LANDING_PATH = f"/Volumes/{CATALOG}/{LANDING_SCHEMA}/storage_files"

PIPELINE_NAME = "carrinho-abandonado"

# COMMAND ----------

# DBTITLE 1,Fontes - mapeamento das 8 tabelas do dump Hybris
DRIVE_FOLDER_ID = "1rUoWqCZuMgXKiXXQHLqs6pxI9kQRE7ns"

FONTES = {
    "tb_carts": {"zip": "tb_carts.zip", "file": "tb_carts.parquet", "format": "parquet"},
    "tb_cartentries": {"zip": "tb_cartentries.zip", "file": "tb_cartentries.parquet", "format": "parquet"},
    "tb_addresses": {"zip": "tb_addresses.zip", "file": "tb_addresses.parquet", "format": "parquet"},
    "tb_paymentinfos": {"zip": "tb_paymentinfos.zip", "file": "tb_paymentinfos.parquet", "format": "parquet"},
    "tb_users": {"zip": None, "file": "tb_users.csv", "format": "csv", "sep": "|"},
    "tb_regions": {"zip": None, "file": "tb_regions.csv", "format": "csv", "sep": "|"},
    "tb_paymentmodes": {"zip": None, "file": "tb_paymentmodes.csv", "format": "csv", "sep": "|"},
    "tb_cmssitelp": {"zip": None, "file": "tb_cmssitelp.csv", "format": "csv", "sep": "|"},
}

print(f"✓ Variables carregadas | Catalog: {CATALOG} | {len(FONTES)} fontes mapeadas")
