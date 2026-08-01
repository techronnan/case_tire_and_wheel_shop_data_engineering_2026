# Databricks notebook source
# DBTITLE 1,GoldPerguntasNegocio
# MAGIC %run ../0_config/0-Init

# COMMAND ----------

fato_carrinhos = spark.table(f"{SILVER}.fato_carrinhos")
fato_itens = spark.table(f"{SILVER}.fato_carrinho_itens")
dim_enderecos = spark.table(f"{SILVER}.dim_enderecos")

itens_com_data = fato_itens.join(
    fato_carrinhos.select("id_carrinho", "dt_criacao"), "id_carrinho"
).withColumn("dt_mes", trunc("dt_criacao", "month"))

# COMMAND ----------

# DBTITLE 1,Q1 - produtos com mais carrinhos abandonados
rpt_produtos_mais_abandonados = (
    itens_com_data.groupBy("id_produto")
    .agg(
        countDistinct("id_carrinho").alias("qt_carrinhos_abandonados"),
        _sum("qt_produto").alias("qt_itens_abandonados"),
    )
    .orderBy(col("qt_carrinhos_abandonados").desc())
)
process_data_load(rpt_produtos_mais_abandonados, f"{GOLD}.rpt_produtos_mais_abandonados")

# COMMAND ----------

# DBTITLE 1,Q2 - duplas de produtos que mais aparecem juntas
itens_a = itens_com_data.select("id_carrinho", col("id_produto").alias("id_produto_a"))
itens_b = itens_com_data.select("id_carrinho", col("id_produto").alias("id_produto_b"))

rpt_duplas_produtos_abandonados = (
    itens_a.join(itens_b, on="id_carrinho")
    .filter(col("id_produto_a") < col("id_produto_b"))  # evita par duplicado/auto-par
    .groupBy("id_produto_a", "id_produto_b")
    .agg(countDistinct("id_carrinho").alias("qt_carrinhos_abandonados"))
    .orderBy(col("qt_carrinhos_abandonados").desc())
)
process_data_load(rpt_duplas_produtos_abandonados, f"{GOLD}.rpt_duplas_produtos_abandonados")

# COMMAND ----------

# DBTITLE 1,Q3 - produtos com aumento de abandono (mes a mes)
por_produto_mes = itens_com_data.groupBy("id_produto", "dt_mes").agg(
    countDistinct("id_carrinho").alias("qt_carrinhos_abandonados")
)

janela_produto = Window.partitionBy("id_produto").orderBy("dt_mes")

tendencia = por_produto_mes.withColumn(
    "qt_carrinhos_mes_anterior", lag("qt_carrinhos_abandonados").over(janela_produto)
).withColumn("var_qt_carrinhos", col("qt_carrinhos_abandonados") - col("qt_carrinhos_mes_anterior"))

ultimo_mes = itens_com_data.agg(_max("dt_mes")).first()[0]

rpt_produtos_aumento_abandono = (
    tendencia.filter((col("dt_mes") == lit(ultimo_mes)) & (col("var_qt_carrinhos") > 0))
    .orderBy(col("var_qt_carrinhos").desc())
)
process_data_load(rpt_produtos_aumento_abandono, f"{GOLD}.rpt_produtos_aumento_abandono")

# COMMAND ----------

# DBTITLE 1,Q4 - produtos novos e volume no primeiro mes
# "Produto novo"/"mes de lancamento" = primeiro mes em que o produto aparece no
# dataset de carrinhos (sem data de cadastro de catalogo nos dados fornecidos).
primeiro_mes_produto = itens_com_data.groupBy("id_produto").agg(_min("dt_mes").alias("dt_mes_lancamento"))

rpt_produtos_novos_ultimo_mes = (
    itens_com_data.join(primeiro_mes_produto, on="id_produto")
    .filter((col("dt_mes") == col("dt_mes_lancamento")) & (col("dt_mes_lancamento") == lit(ultimo_mes)))
    .groupBy("id_produto", "dt_mes_lancamento")
    .agg(countDistinct("id_carrinho").alias("qt_carrinhos_primeiro_mes"))
    .orderBy(col("qt_carrinhos_primeiro_mes").desc())
)
process_data_load(rpt_produtos_novos_ultimo_mes, f"{GOLD}.rpt_produtos_novos_ultimo_mes")

# COMMAND ----------

# DBTITLE 1,Q5 - estados com mais abandonos
# id_endereco (endereco de pagamento) so cobre ~6 carrinhos em 16M - quase ninguem
# chega nessa etapa do checkout antes de abandonar. cd_cep_calculado (CEP usado pra
# simular frete, preenchido bem mais cedo no funil) cobre ~11,5% dos carrinhos ->
# resolvido pra UF via faixa oficial de CEP dos Correios. sg_uf do endereco de
# pagamento tem prioridade quando existe (mais preciso que faixa de CEP), o resto
# cai pro CEP calculado.
FAIXAS_CEP_UF = [
    (1000000, 19999999, "SP"), (20000000, 28999999, "RJ"), (29000000, 29999999, "ES"),
    (30000000, 39999999, "MG"), (40000000, 48999999, "BA"), (49000000, 49999999, "SE"),
    (50000000, 56999999, "PE"), (57000000, 57999999, "AL"), (58000000, 58999999, "PB"),
    (59000000, 59999999, "RN"), (60000000, 63999999, "CE"), (64000000, 64999999, "PI"),
    (65000000, 65999999, "MA"), (66000000, 68899999, "PA"), (68900000, 68999999, "AP"),
    (69000000, 69299999, "AM"), (69300000, 69399999, "RR"), (69400000, 69899999, "AM"),
    (69900000, 69999999, "AC"), (70000000, 72799999, "DF"), (72800000, 72999999, "GO"),
    (73000000, 73699999, "DF"), (73700000, 76799999, "GO"), (76800000, 76999999, "RO"),
    (77000000, 77999999, "TO"), (78000000, 78899999, "MT"), (78900000, 78999999, "RO"),
    (79000000, 79999999, "MS"), (80000000, 87999999, "PR"), (88000000, 89999999, "SC"),
    (90000000, 99999999, "RS"),
]
faixas_cep_uf = spark.createDataFrame(FAIXAS_CEP_UF, ["cep_ini", "cep_fim", "sg_uf_cep"])

carrinhos_com_uf = (
    fato_carrinhos.join(dim_enderecos, on="id_endereco", how="left")
    .withColumn("cep_num", col("cd_cep_calculado").cast("int"))
    .join(
        broadcast(faixas_cep_uf),
        col("cep_num").between(col("cep_ini"), col("cep_fim")),
        "left",
    )
    .withColumn("sg_uf_resolvido", coalesce(col("sg_uf"), col("sg_uf_cep")))
)

rpt_estados_mais_abandonos = (
    carrinhos_com_uf.groupBy(col("sg_uf_resolvido").alias("sg_uf"))
    .agg(countDistinct("id_carrinho").alias("qt_carrinhos_abandonados"))
    .orderBy(col("qt_carrinhos_abandonados").desc())
)
process_data_load(rpt_estados_mais_abandonos, f"{GOLD}.rpt_estados_mais_abandonos")
