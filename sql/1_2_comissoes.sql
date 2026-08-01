-- Setup pra testar (opcional) — tabela + dado de exemplo do enunciado.
CREATE TABLE comissoes (
    comprador VARCHAR NOT NULL
    ,vendedor VARCHAR NOT NULL
    ,dataPgto DATE NOT NULL
    ,valor FLOAT NOT NULL
);
INSERT INTO comissoes VALUES
    ('Leonardo', 'Bruno',   DATE '2000-01-01', 200.00),
    ('Leonardo', 'Matheus', DATE '2003-09-27', 1024.00),
    ('Leonardo', 'Lucas',   DATE '2006-06-26', 512.00),
    ('Marcos',   'Lucas',   DATE '2020-12-17', 100.00),
    ('Marcos',   'Lucas',   DATE '2002-03-22', 10.00),
    ('Cinthia',  'Lucas',   DATE '2021-03-20', 500.00),
    ('Mateus',   'Bruno',   DATE '2007-06-02', 400.00),
    ('Mateus',   'Bruno',   DATE '2006-06-26', 400.00),
    ('Mateus',   'Bruno',   DATE '2015-06-26', 200.00);

-- Parte 1.2 — Comissões
-- Vendedor entra se as 3 maiores comissões dele já somam >= 1024 (se as 3 maiores
-- não chegam lá, nenhum subconjunto menor chegaria).
-- Resultado esperado: Lucas, Matheus (Bruno NAO entra)

WITH comissoes_ranqueadas AS (
    SELECT
        vendedor,
        valor,
        ROW_NUMBER() OVER (PARTITION BY vendedor ORDER BY valor DESC) AS rn
    FROM comissoes
)

SELECT vendedor
FROM comissoes_ranqueadas
WHERE rn <= 3
GROUP BY vendedor
HAVING SUM(valor) >= 1024
ORDER BY vendedor ASC;
