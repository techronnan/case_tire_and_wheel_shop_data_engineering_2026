-- Setup pra testar (opcional) — tabela + dado de exemplo do enunciado.
CREATE TABLE colaboradores (
    id INTEGER NOT NULL
    , nome VARCHAR NOT NULL
    , salario INTEGER NOT NULL
    , lider_id INTEGER
    , UNIQUE(id)
);
INSERT INTO colaboradores VALUES
    (40, 'Helen', 1500, 50),
    (50, 'Bruno', 3000, 10),
    (10, 'Leonardo', 4500, 20),
    (20, 'Marcos', 10000, NULL),
    (70, 'Mateus', 1500, 10),
    (60, 'Cinthia', 2000, 70),
    (30, 'Wilian', 1501, 50);

-- Parte 1.3 — Organização Empresarial
-- O chefe indireto "mais baixo na hierarquia" que ganha o dobro = o primeiro chefe
-- subindo a cadeia (chefe direto, depois chefe do chefe...) que bate a condição de
-- salário — porque quem está mais perto do funcionário sempre tem mais chefes
-- indiretos acima de si do que quem está mais longe.
-- Resultado esperado: 10->20, 20->NULL, 30->10, 40->50, 50->20, 60->10, 70->10

WITH RECURSIVE hierarquia AS (
    SELECT
        c.id AS funcionario_id,
        c.salario AS salario_funcionario,
        c.lider_id AS chefe_id,
        1 AS nivel
    FROM colaboradores c
    WHERE c.lider_id IS NOT NULL

    UNION ALL

    SELECT
        h.funcionario_id,
        h.salario_funcionario,
        chefe_atual.lider_id AS chefe_id,
        h.nivel + 1 AS nivel
    FROM hierarquia h
    JOIN colaboradores chefe_atual ON chefe_atual.id = h.chefe_id
    WHERE chefe_atual.lider_id IS NOT NULL
),

candidatos AS (
    SELECT h.funcionario_id, h.chefe_id, h.nivel
    FROM hierarquia h
    JOIN colaboradores chefe ON chefe.id = h.chefe_id
    WHERE chefe.salario >= 2 * h.salario_funcionario
),

melhor_chefe AS (
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
LEFT JOIN melhor_chefe mc ON mc.funcionario_id = c.id AND mc.rn = 1
ORDER BY c.id ASC;
