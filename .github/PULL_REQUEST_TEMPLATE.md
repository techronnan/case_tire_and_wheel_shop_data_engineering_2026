## Descrição

<!-- O que mudou e por quê -->

### Escopo

- [ ] Novo(s) Job(s)/Workflow(s) do GitHub Actions
- [ ] Novo(s) notebook(s) (Bronze/Silver/Gold/config)
- [ ] Alteração em notebook(s) existente(s)
- [ ] Alteração no Job/Bundle (`databricks.yml`, `resources/jobs/*.yml`)
- [ ] Catalog/schema/tabela novo

## Evidências

<!-- Print ou link da run com sucesso (check `deploy` deste PR, ou
`databricks bundle run ... -t dev` manual) -->

## Homologação

<!-- Evidência de que o dado está correto: contagem de linhas, amostra do
resultado, ou que a task `qualidade_dados` passou -->

## Ambiente de Produção

<!-- Ação manual necessária depois do merge? (ex.: despausar o schedule,
rodar manualmente a primeira vez). Se não houver, escreva "Nenhuma". -->

### Checklist

- [ ] `databricks bundle validate` passou (dev e prod, se mexeu no bundle)
- [ ] Notebooks/scripts alterados compilam (`python -m py_compile`)
- [ ] Segue a convenção de nomes/prefixo de coluna do projeto (`docs/SPEC.md`)
- [ ] Escrita sempre via `process_data_load` (nunca `spark.write`/`saveAsTable` direto) — mantém upsert e log consistentes
- [ ] Se mexeu em Silver: `check_quality` cobre a(s) tabela(s) nova(s)/alterada(s)
- [ ] Nenhum dado sensível (nome da empresa, secret, token) commitado
