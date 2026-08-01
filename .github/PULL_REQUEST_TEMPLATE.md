## Resumo

<!-- O que mudou e por quê -->

## Tipo de mudança

- [ ] Notebook (Bronze/Silver/Gold/config)
- [ ] Job/Bundle (`databricks.yml`, `resources/jobs/*.yml`)
- [ ] CI/CD (`.github/workflows/*.yml`, `scripts/*.py`)
- [ ] Documentação

## Checklist

- [ ] `databricks bundle validate` rodou sem erro (dev e prod, se mexeu no bundle)
- [ ] Notebooks/scripts alterados compilam (`python -m py_compile`)
- [ ] Se mudou schema/catalog/nome de tabela: atualizei os lugares que referenciam
- [ ] Se mudou o Job: o check `deploy` deste PR passou

## Teste manual (se aplicável)

<!-- Rodou `databricks bundle run ... -t dev` manualmente pra confirmar? Cole o
resultado ou o link da run aqui. -->

## Impacto

<!-- Isso muda o que roda em prod no próximo merge? Precisa de ação manual
depois do merge (ex.: despausar o schedule, rodar uma vez)? -->
