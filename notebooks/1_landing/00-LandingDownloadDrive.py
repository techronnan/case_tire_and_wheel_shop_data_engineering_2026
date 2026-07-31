# Databricks notebook source
# DBTITLE 1,LandingDownloadDrive
# MAGIC %pip install gdown --quiet

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ../0_config/0-Init

# COMMAND ----------

dbutils.widgets.dropdown("force_download", "false", ["true", "false"])
force_download = dbutils.widgets.get("force_download") == "true"

import gdown

# COMMAND ----------

todos_presentes = all(
    os.path.exists(os.path.join(LANDING_PATH, f["zip"] or f["file"])) for f in FONTES.values()
)

if todos_presentes and not force_download:
    print(f"Todos os arquivos ja presentes em {LANDING_PATH} — pulando download da pasta")
else:
    print(f"Baixando pasta drive://{DRIVE_FOLDER_ID} -> {LANDING_PATH}")
    gdown.download_folder(id=DRIVE_FOLDER_ID, output=LANDING_PATH, quiet=False, use_cookies=False)

# COMMAND ----------

faltando = []
for nome, f in FONTES.items():
    download_name = f["zip"] or f["file"]
    dest_path = os.path.join(LANDING_PATH, download_name)

    if not os.path.exists(dest_path):
        faltando.append(f"{nome} -> esperava '{download_name}' em {LANDING_PATH}")
        continue

    if f["zip"]:
        extract_path = os.path.join(LANDING_PATH, f["file"])
        if not os.path.exists(extract_path) or force_download:
            with zipfile.ZipFile(dest_path) as z:
                z.extract(f["file"], path=LANDING_PATH)
        print(f"  [OK] {nome} -> {extract_path}")
    else:
        print(f"  [OK] {nome} -> {dest_path}")

if faltando:
    raise FileNotFoundError(
        "Arquivo(s) nao encontrado(s) apos o download da pasta do Drive (confira nome "
        "do arquivo e compartilhamento 'Qualquer pessoa com o link -> Leitor'):\n"
        + "\n".join(faltando)
    )

print(f"✓ Landing concluido | {len(FONTES)} arquivos em {LANDING_PATH}")
