# Case — Engenheiro de Dados

Entrega de um teste técnico para vaga de Engenheiro de Dados, dividido em duas partes.

A primeira é SQL: um ranking de campeonato por pontos, uma consulta sobre comissões
de vendedores (soma de subconjuntos de transferências) e uma consulta recursiva de
hierarquia de funcionários (achar o chefe indireto mais próximo que ganha pelo menos
o dobro do salário). Roda como notebook + Job (`wf_pneustore_sql_parte1`), com o
dado de exemplo do próprio enunciado — ver [notebooks/parte1_sql/](notebooks/parte1_sql/):

- [`00-Setup.py`](notebooks/parte1_sql/00-Setup.py) — cria as 4 tabelas de exemplo do enunciado (`times`, `jogos`, `comissoes`, `colaboradores`)
- [`01-Campeonato.py`](notebooks/parte1_sql/01-Campeonato.py) — ranking por pontos → `rpt_campeonato`
- [`02-Comissoes.py`](notebooks/parte1_sql/02-Comissoes.py) — vendedores com até 3 comissões somando 1024+ → `rpt_comissoes_vendedores`
- [`03-OrganizacaoEmpresarial.py`](notebooks/parte1_sql/03-OrganizacaoEmpresarial.py) — chefe indireto mais próximo que ganha o dobro → `rpt_organizacao_chefes`

```mermaid
flowchart LR
    S[00-Setup<br/>cria times, jogos,<br/>comissoes, colaboradores] --> C1[01-Campeonato]
    S --> C2[02-Comissoes]
    S --> C3[03-OrganizacaoEmpresarial]
    C1 --> R1[(rpt_campeonato)]
    C2 --> R2[(rpt_comissoes_vendedores)]
    C3 --> R3[(rpt_organizacao_chefes)]
```

Job: `wf_pneustore_sql_parte1`.

A segunda parte é uma análise de carrinho abandonado num e-commerce (dataset SAP
Hybris/Commerce Cloud, ~33M linhas em 8 tabelas: carrinhos, itens, usuários,
endereços, formas de pagamento etc.). O dado bruto é grande demais pra caber no
git, então fica hospedado numa pasta do Google Drive e é baixado em runtime.

## Arquitetura

```mermaid
flowchart LR
    Setup[0_config<br/>4-SetupCatalog] --> Landing[1_landing<br/>00-LandingDownloadDrive]
    Landing --> Bronze[2_bronze<br/>01-BronzeIngestao]
    Bronze --> SilverDim[3_silver<br/>01-SilverDimensoes]
    Bronze --> SilverFat[3_silver<br/>02-SilverFatos]
    SilverDim --> Qualidade[3_silver<br/>03-QualidadeDados]
    SilverFat --> Qualidade
    Qualidade --> GoldPerguntas[4_gold<br/>01-GoldPerguntasNegocio]
    Qualidade --> GoldRelatorios[4_gold<br/>02-GoldRelatorios]
    Qualidade --> GoldExport[4_gold<br/>03-GoldExportTop50]
```

Job: `wf_pneustore_carrinho_abandonado`. Landing, Bronze, Silver e Gold rodam como
notebooks Databricks orquestrados por esse Job (Databricks Asset Bundles), com
upsert por chave em Bronze/Silver — não é um overwrite cego, uma nova execução
atualiza só o que mudou. `QualidadeDados` bloqueia a Gold se alguma tabela Silver
falhar nos checks (linha zero, chave nula, chave duplicada).

- [`notebooks/1_landing/`](notebooks/1_landing/) — baixa as 8 tabelas do dump do Google Drive pro Volume
- [`notebooks/2_bronze/`](notebooks/2_bronze/) — ingestão bruta, schema preservado como veio da fonte
- [`notebooks/3_silver/`](notebooks/3_silver/) — tipagem, conformidade e enriquecimento (ex.: resolução
  de UF do carrinho via faixa de CEP, já que o endereço de pagamento raramente é preenchido)
- [`notebooks/4_gold/`](notebooks/4_gold/) — as 5 perguntas de negócio, os 2 relatórios de acompanhamento e o export top50

## Casos de uso (Parte 2)

Cada pergunta da prova vira uma tabela Gold, gerada por
[`notebooks/4_gold/01-GoldPerguntasNegocio.py`](notebooks/4_gold/01-GoldPerguntasNegocio.py):

| Pergunta | Tabela |
|---|---|
| Produtos com mais carrinhos abandonados | `gold.rpt_produtos_mais_abandonados` |
| Duplas de produtos que mais aparecem juntas | `gold.rpt_duplas_produtos_abandonados` |
| Produtos com aumento de abandono mês a mês | `gold.rpt_produtos_aumento_abandono` |
| Produtos novos e volume no primeiro mês | `gold.rpt_produtos_novos_ultimo_mes` |
| Estados com mais abandonos | `gold.rpt_estados_mais_abandonos` |

Os dois relatórios de acompanhamento (produto × mês e por data — quantidade de
carrinhos, itens e valor não faturado) saem de
[`notebooks/4_gold/02-GoldRelatorios.py`](notebooks/4_gold/02-GoldRelatorios.py).

O export final — `.txt` com os 50 carrinhos de maior valor, no layout pipe-delimited
pedido na prova — sai de
[`notebooks/4_gold/03-GoldExportTop50.py`](notebooks/4_gold/03-GoldExportTop50.py).

## Conteúdo

- `case/` — enunciado original (CASO.md) e descrição da vaga (VAGA.md)
- `notebooks/parte1_sql/` — setup (tabelas de exemplo) + as 3 queries da Parte 1
- `notebooks/0_config/` — catalog, paths, mapeamento das fontes, funções compartilhadas
- `notebooks/1_landing/` — download do Google Drive
- `notebooks/2_bronze/` — ingestão bruta das 8 tabelas
- `notebooks/3_silver/` — tipagem e conformidade
- `notebooks/4_gold/` — perguntas de negócio, relatórios e export
- `databricks.yml` + `resources/jobs/` — Asset Bundle

## Evidências de execução

Prints reais das execuções no Databricks (workspace dev), pra mostrar não só que o
código existe, mas que ele roda e devolve o resultado esperado.

### Parte 1 (SQL)

Job `wf_pneustore_sql_parte1`: setup cria as 4 tabelas de exemplo, depois as 3
queries rodam em paralelo.

| | |
|---|---|
| ![Job iniciando](img/parte1-sql-job-rodando.png) | Job disparado — `setup` rodando, as 3 queries aguardando |
| ![Job concluído](img/parte1-sql-job-sucesso.png) | Job concluído — `campeonato`, `comissoes` e `organizacao_empresarial` com sucesso |
| ![Setup](img/parte1-sql-setup-notebook.png) | `00-Setup`: criação das 4 tabelas de exemplo (aqui, `colaboradores`) |

Resultado real de cada query (aberto interativo no notebook, não só o log de gravação):

| Query | Resultado |
|---|---|
| 1.1 Campeonato | ![Resultado campeonato](img/parte1-sql-campeonato-resultado.png) |
| 1.2 Comissões | ![Resultado comissões](img/parte1-sql-comissoes-resultado.png) |
| 1.3 Organização Empresarial | ![Resultado organização empresarial](img/parte1-sql-organizacao-resultado.png) |

Log de gravação de cada task do Job (código + confirmação de linhas gravadas):

| | |
|---|---|
| ![Log campeonato](img/parte1-sql-campeonato-log.png) | `01-Campeonato` → `rpt_campeonato`, 5 linhas |
| ![Log comissões](img/parte1-sql-comissoes-log.png) | `02-Comissoes` → `rpt_comissoes_vendedores`, 2 linhas |
| ![Log organização](img/parte1-sql-organizacao-log.png) | `03-OrganizacaoEmpresarial` → `rpt_organizacao_chefes`, 7 linhas |

### Parte 2 (Carrinho Abandonado)

Job `wf_pneustore_carrinho_abandonado`: pipeline completo, Landing → Bronze →
Silver → Qualidade → Gold.

| | |
|---|---|
| ![Job iniciando](img/parte2-job-rodando.png) | Job disparado — `setup` rodando |
| ![Job concluído](img/parte2-job-sucesso.png) | Job completo com sucesso — DAG inteiro, ~5min |
| ![Catálogo](img/parte2-catalog-tabelas-gold.png) | Unity Catalog: as 7 tabelas Gold + o volume `exports` com o `.txt` do top50 |
| ![E-mail de notificação](img/parte2-email-notificacao.png) | E-mail automático de sucesso do Job (`email_notifications.on_success`) |

Log de cada etapa (código + contagem real de linhas gravadas):

| Etapa | Evidência |
|---|---|
| `landing_download` — 8 arquivos baixados do Drive | ![Landing](img/parte2-landing-log.png) |
| `bronze_ingestao` — 8 tabelas, ~16M linhas em `tb_carts` | ![Bronze](img/parte2-bronze-log.png) |
| `silver_dimensoes` — `dim_usuarios`, `dim_enderecos` etc. | ![Silver dimensões](img/parte2-silver-dimensoes-log.png) |
| `silver_fatos` — `fato_carrinhos`, `fato_carrinho_itens` | ![Silver fatos](img/parte2-silver-fatos-log.png) |
| `qualidade_dados` — 8 tabelas verificadas, todas OK | ![Qualidade de dados](img/parte2-qualidade-dados-log.png) |
| `gold_export_top50` — 50 carrinhos, 217 linhas no `.txt` | ![Export top50](img/parte2-export-top50-log.png) |

Resposta real de cada pergunta (o #1 do ranking — a tabela completa tem uma linha
por produto/dupla/mês, o total de linhas só diz quantos produtos existem no
ranking, não responde a pergunta sozinho). Q5 documentada em detalhe mais acima,
na seção de arquitetura, por causa da resolução via CEP.

| Pergunta | Resposta (#1 do ranking) | Evidência |
|---|---|---|
| Q1 — produto com mais carrinhos abandonados | produto `8797277388801`: 33.617 carrinhos, 95.386 itens abandonados | ![Q1](img/parte2-q1-resultado.png) |
| Q2 — dupla de produtos que mais aparece junta | `8797983080449` + `8800160120833`: 1.205 carrinhos com os dois juntos | ![Q2](img/parte2-q2-resultado.png) |
| Q3 — produto com maior aumento de abandono no último mês | produto `8800160153601` em jul/2022: 960 → 2.803 carrinhos (+1.843) | ![Q3](img/parte2-q3-resultado.png) |
| Q4 — produto novo com mais carrinhos no 1º mês | produto `8808152465409`, lançado jul/2022: 38 carrinhos no mês de estreia | ![Q4](img/parte2-q4-resultado.png) |

(Ranking completo — todos os produtos/duplas/meses, não só o #1 — nas imagens e
nas tabelas `gold.rpt_*` correspondentes.)
