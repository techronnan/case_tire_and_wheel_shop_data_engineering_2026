# Databricks notebook source
# DBTITLE 1,QualidadeDados
# MAGIC %run ../0_config/0-Init

# COMMAND ----------

# Checks simples pos-Silver: linha>0, PK sem nulo, PK sem duplicata. Gold so roda
# se tudo passar aqui - falha bloqueia a camada Gold e dispara o e-mail de erro.
TABELAS = {
    f"{SILVER}.dim_regioes": "id_regiao",
    f"{SILVER}.dim_formas_pagamento": "id_forma_pagamento",
    f"{SILVER}.dim_sites": "id_site",
    f"{SILVER}.dim_pagamento_parcelas": "id_info_pagamento",
    f"{SILVER}.dim_usuarios": "id_usuario",
    f"{SILVER}.dim_enderecos": "id_endereco",
    f"{SILVER}.fato_carrinhos": "id_carrinho",
    f"{SILVER}.fato_carrinho_itens": "id_item_carrinho",
}

falhas = []
for nome_tabela, chave in TABELAS.items():
    resultado = check_quality(nome_tabela, chave)
    falhas.extend(resultado)
    print(f"  [{'OK' if not resultado else 'FALHOU'}] {nome_tabela}")

if falhas:
    raise ValueError("Falhas de qualidade de dados:\n" + "\n".join(falhas))

print(f"✓ Qualidade de dados OK | {len(TABELAS)} tabelas verificadas")
