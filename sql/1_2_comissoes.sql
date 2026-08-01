-- Parte 1.2 — Comissões
-- Vendedor entra se as 3 maiores comissões dele já somam >= 1024 (se as 3 maiores
-- não chegam lá, nenhum subconjunto menor chegaria).

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
