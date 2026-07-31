-- Prova CantuStore — Parte 1.1 — Campeonato
-- Ranking de times por pontos (vitória=3, empate=1, derrota=0), desc por pontos,
-- empate desempatado por time_id asc. Times sem nenhuma partida entram com 0 pontos
-- (por isso o LEFT JOIN a partir de `times`, não um JOIN a partir de `jogos`).

WITH resultados AS (
    -- Perspectiva do mandante em cada jogo
    SELECT
        mandante_time AS time_id,
        CASE
            WHEN mandante_gols > visitante_gols THEN 3
            WHEN mandante_gols = visitante_gols THEN 1
            ELSE 0
        END AS pontos
    FROM jogos

    UNION ALL

    -- Perspectiva do visitante em cada jogo
    SELECT
        visitante_time AS time_id,
        CASE
            WHEN visitante_gols > mandante_gols THEN 3
            WHEN visitante_gols = mandante_gols THEN 1
            ELSE 0
        END AS pontos
    FROM jogos
)

SELECT
    t.time_id,
    t.time_nome,
    COALESCE(SUM(r.pontos), 0) AS num_pontos
FROM times t
LEFT JOIN resultados r
    ON r.time_id = t.time_id
GROUP BY t.time_id, t.time_nome
ORDER BY num_pontos DESC, t.time_id ASC;

-- Validação contra o exemplo da prova (5 jogos):
-- 20 -> 4 pts (derrota, vitória, empate) | 50 -> 4 pts (empate, vitória)
-- 10 -> 3 pts (derrota, vitória)          | 30 -> 3 pts (vitória, derrota, derrota)
-- 40 -> 0 pts (não jogou)
-- Resultado esperado: 20(4), 50(4), 10(3), 30(3), 40(0) — desempate 20<50 e 10<30 por time_id.
