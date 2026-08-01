-- Setup pra testar (opcional) — tabelas + dado de exemplo do enunciado.
CREATE TABLE times (
    time_id INTEGER NOT NULL
    ,time_nome VARCHAR NOT NULL
    ,UNIQUE(time_id)
);
INSERT INTO times VALUES
    (10, 'Financeiro'), (20, 'Marketing'), (30, 'Logística'), (40, 'TI'), (50, 'Dados');

CREATE TABLE jogos (
    jogo_id INTEGER NOT NULL
    , mandante_time INTEGER NOT NULL
    , visitante_time INTEGER NOT NULL
    , mandante_gols INTEGER NOT NULL
    , visitante_gols INTEGER NOT NULL
    , UNIQUE(jogo_id)
);
INSERT INTO jogos VALUES
    (1, 30, 20, 1, 0), (2, 10, 20, 1, 2), (3, 20, 50, 2, 2), (4, 10, 30, 1, 0), (5, 30, 50, 0, 1);

-- Parte 1.1 — Campeonato
-- Pontos por time (vitória=3, empate=1, derrota=0). LEFT JOIN a partir de `times`
-- pra time sem partida entrar com 0.
-- Resultado esperado: 20(4), 50(4), 10(3), 30(3), 40(0)

WITH resultados AS (
    SELECT mandante_time AS time_id,
        CASE WHEN mandante_gols > visitante_gols THEN 3
             WHEN mandante_gols = visitante_gols THEN 1 ELSE 0 END AS pontos
    FROM jogos
    UNION ALL
    SELECT visitante_time AS time_id,
        CASE WHEN visitante_gols > mandante_gols THEN 3
             WHEN visitante_gols = mandante_gols THEN 1 ELSE 0 END AS pontos
    FROM jogos
)

SELECT
    t.time_id,
    t.time_nome,
    COALESCE(SUM(r.pontos), 0) AS num_pontos
FROM times t
LEFT JOIN resultados r ON r.time_id = t.time_id
GROUP BY t.time_id, t.time_nome
ORDER BY num_pontos DESC, t.time_id ASC;
