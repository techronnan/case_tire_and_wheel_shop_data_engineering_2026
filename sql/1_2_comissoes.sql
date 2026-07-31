-- Prova CantuStore — Parte 1.2 — Comissões
-- Lista vendedores para os quais existe um subconjunto de até 3 comissões cuja soma
-- é >= 1024. Como queremos saber se ALGUM subconjunto de tamanho <=3 atinge 1024,
-- e queremos o MAIOR valor possível somando no máximo 3 valores, o subconjunto ótimo
-- é sempre "as 3 maiores comissões do vendedor" (ou menos, se ele tiver menos de 3).
-- Se nem as 3 maiores juntas chegam a 1024, nenhum outro subconjunto de até 3 chegaria.

WITH comissoes_ranqueadas AS (
    SELECT
        vendedor,
        valor,
        ROW_NUMBER() OVER (PARTITION BY vendedor ORDER BY valor DESC) AS rn
    FROM comissoes
)

SELECT
    vendedor
FROM comissoes_ranqueadas
WHERE rn <= 3
GROUP BY vendedor
HAVING SUM(valor) >= 1024
ORDER BY vendedor ASC;

-- Validação contra o exemplo da prova:
-- Lucas   -> top3 = 512+500+100 = 1112 >= 1024 -> listado
-- Matheus -> top1 = 1024        >= 1024 -> listado
-- Bruno   -> top3 = 400+400+200 = 1000 <  1024 -> NÃO listado
