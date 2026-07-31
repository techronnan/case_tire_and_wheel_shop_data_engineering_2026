-- Prova CantuStore — Parte 1.3 — Organização Empresarial
--
-- Para cada funcionário, achar o chefe indireto "de classificação mais baixa na
-- hierarquia" (ou seja, o que tem MAIS chefes indiretos acima de si — o mais
-- próximo do funcionário na cadeia) que ganha pelo menos o dobro do salário dele.
--
-- Raciocínio-chave: numa cadeia funcionário -> D1 (chefe direto) -> D2 -> D3 -> ...,
-- D1 sempre tem MAIS chefes indiretos que D2 (que por sua vez tem mais que D3, etc.),
-- porque o conjunto de chefes indiretos de D2 é subconjunto do de D1. Logo "chefe
-- indireto de classificação mais baixa que satisfaz a condição" = o PRIMEIRO chefe,
-- subindo a cadeia a partir do chefe direto, cujo salário >= 2x o do funcionário.
--
-- Requer WITH RECURSIVE (suportado em Databricks SQL, PostgreSQL, SQL Server, etc.).

WITH RECURSIVE hierarquia AS (
    -- nível 1: o chefe direto de cada funcionário
    SELECT
        c.id AS funcionario_id,
        c.salario AS salario_funcionario,
        c.lider_id AS chefe_id,
        1 AS nivel
    FROM colaboradores c
    WHERE c.lider_id IS NOT NULL

    UNION ALL

    -- sobe um nível: o chefe do chefe atual da cadeia
    SELECT
        h.funcionario_id,
        h.salario_funcionario,
        chefe_atual.lider_id AS chefe_id,
        h.nivel + 1 AS nivel
    FROM hierarquia h
    JOIN colaboradores chefe_atual
        ON chefe_atual.id = h.chefe_id
    WHERE chefe_atual.lider_id IS NOT NULL
),

candidatos AS (
    -- chefes indiretos que ganham pelo menos o dobro do funcionário
    SELECT
        h.funcionario_id,
        h.chefe_id,
        h.nivel
    FROM hierarquia h
    JOIN colaboradores chefe ON chefe.id = h.chefe_id
    WHERE chefe.salario >= 2 * h.salario_funcionario
),

melhor_chefe AS (
    -- entre os candidatos, o de menor nível = o mais próximo do funcionário na
    -- cadeia = o de classificação mais baixa na hierarquia (ver raciocínio acima)
    SELECT
        funcionario_id,
        chefe_id,
        ROW_NUMBER() OVER (PARTITION BY funcionario_id ORDER BY nivel ASC) AS rn
    FROM candidatos
)

SELECT
    c.id AS id_funcionario,
    mc.chefe_id AS id_chefe
FROM colaboradores c
LEFT JOIN melhor_chefe mc
    ON mc.funcionario_id = c.id
    AND mc.rn = 1
ORDER BY c.id ASC;
