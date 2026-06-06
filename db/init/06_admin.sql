--------------------------------------------------------------------
--- Triggers para sincronizar inserções em CONSTRUCTORS e DRIVERS ---
--------------------------------------------------------------------

--- Trigger para inserção em CONSTRUCTORS ---
CREATE OR REPLACE FUNCTION tg_sync_constructor_to_users()
RETURNS TRIGGER AS $$
BEGIN
    -- Se o login já existir, a constraint UNIQUE de 'users' vai quebrar
    -- e dar ROLLBACK em toda a transação (incluindo o constructor)
    INSERT INTO users (login, password, tipo, id_original)
    VALUES (
        NEW.constructor_ref || '_c', 
        crypt(NEW.constructor_ref, gen_salt('bf', 10)), 
        'Escuderia', 
        NEW.constructor_ref
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_after_constructor_insert
AFTER INSERT ON constructors
FOR EACH ROW
EXECUTE FUNCTION tg_sync_constructor_to_users();

--- Trigger de deleção para CONSTRUCTORS ---
CREATE OR REPLACE FUNCTION tg_sync_delete_constructor_to_users()
RETURNS TRIGGER AS $$
BEGIN
    -- Remove o usuário correspondente usando o padrão '_c'
    DELETE FROM users WHERE login = OLD.constructor_ref || '_c';
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_after_constructor_delete
AFTER DELETE ON constructors
FOR EACH ROW
EXECUTE FUNCTION tg_sync_delete_constructor_to_users();


--- Trigger para inserção em DRIVERS ---
CREATE OR REPLACE FUNCTION tg_sync_driver_to_users()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO users (login, password, tipo, id_original)
    VALUES (
        NEW.driver_ref || '_d', 
        crypt(NEW.driver_ref, gen_salt('bf', 10)), 
        'Piloto', 
        NEW.driver_ref
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_after_driver_insert
AFTER INSERT ON drivers
FOR EACH ROW
EXECUTE FUNCTION tg_sync_driver_to_users();


--- Trigger de deleção para DRIVERS ---
CREATE OR REPLACE FUNCTION tg_sync_delete_driver_to_users()
RETURNS TRIGGER AS $$
BEGIN
    -- Remove o usuário correspondente usando o padrão '_d'
    DELETE FROM users WHERE login = OLD.driver_ref || '_d';
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_after_driver_delete
AFTER DELETE ON drivers
FOR EACH ROW
EXECUTE FUNCTION tg_sync_delete_driver_to_users();


--------------------------------------------------------------------
--- Dashboard de admin
--------------------------------------------------------------------
--- Sumário ---
CREATE OR REPLACE FUNCTION get_db_summary()
RETURNS TABLE(total_drivers BIGINT, total_constructors BIGINT, total_seasons BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*) FROM drivers),
        (SELECT COUNT(*) FROM constructors),
        (SELECT COUNT(*) FROM seasons);
END;
$$ LANGUAGE plpgsql STABLE;


--- Corridas da última temporada ---
DROP FUNCTION IF EXISTS get_latest_season_races();
CREATE OR REPLACE FUNCTION get_latest_season_races()
RETURNS TABLE(race_name TEXT, circuit_name TEXT, race_date DATE, race_time TIME, recorded_laps INT) AS $$
BEGIN
    RETURN QUERY
    WITH max_season AS (
        SELECT id FROM seasons ORDER BY year DESC LIMIT 1
    )
    SELECT 
        r.race_name,
        c.name,
        r.race_date,
        r.race_time,
        MAX(res.laps)::INT
    FROM races r
    JOIN circuits c ON r.circuit_id = c.id
    LEFT JOIN results res ON r.id = res.race_id
    -- Ajuste aqui: Filtra pela ID da temporada mais recente
    WHERE r.season_id = (SELECT id FROM max_season)
    GROUP BY r.id, r.race_name, c.name, r.race_date, r.race_time, r.round
    ORDER BY r.round;
END;
$$ LANGUAGE plpgsql STABLE;


--- Ranking dos construtores da última temporada ---
CREATE OR REPLACE FUNCTION get_latest_constructor_standings()
RETURNS TABLE(constructor_name VARCHAR, total_points NUMERIC) AS $$
BEGIN
    RETURN QUERY
    WITH max_season AS (
        SELECT MAX(year) AS ultimo_ano FROM seasons
    )
    SELECT 
        c.name,
        SUM(res.points)::NUMERIC
    FROM results res
    JOIN races r ON res.race_id = r.id
    JOIN constructors c ON res.constructor_id = c.id
    JOIN seasons s ON r.season_id = s.id
    WHERE s.year = (SELECT ultimo_ano FROM max_season)
    GROUP BY c.id, c.name
    ORDER BY SUM(res.points) DESC;
END;
$$ LANGUAGE plpgsql STABLE;


--- Ranking dos pilotos da última temporada ---
CREATE OR REPLACE FUNCTION get_latest_driver_standings()
RETURNS TABLE(driver_name TEXT, total_points NUMERIC) AS $$
BEGIN
    RETURN QUERY
    WITH max_season AS (
        SELECT MAX(year) AS ultimo_ano FROM seasons
    )
    SELECT 
        (d.given_name || ' ' || d.family_name)::TEXT,
        SUM(res.points)::NUMERIC
    FROM results res
    JOIN races r ON res.race_id = r.id
    JOIN seasons s ON r.season_id = s.id
    JOIN drivers d ON res.driver_id = d.id
    WHERE s.year = (SELECT ultimo_ano FROM max_season)
    GROUP BY d.id, d.given_name, d.family_name
    ORDER BY SUM(res.points) DESC;
END;
$$ LANGUAGE plpgsql STABLE;


--------------------------------------------------------------------
--- Relatórios de admin ---
--------------------------------------------------------------------

--- Índice na FK para acelerar contagens por status ---
---CREATE INDEX idx_results_status_id ON results(status_id);
---DROP INDEX IF EXISTS idx_results_status_id;
--- Desnecessário ter esse índice, não houve quase nenhum ganho de performance; Nos testes,
--- com índice foi 1 ms mais lento do que sem índice


---------------------------------------------------------------------------
-- Relatório 1 (Contagem de resultados por status )--
---------------------------------------------------------------------------
DROP FUNCTION IF EXISTS get_result_status_counts();


CREATE OR REPLACE FUNCTION get_result_status_counts()
RETURNS TABLE(status TEXT, count BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        st.status,
        COUNT(*)::BIGINT
    FROM results res
    JOIN status st ON res.status_id = st.id
    GROUP BY st.status
    ORDER BY COUNT(*) DESC; -- Ponto e vírgula corrigido e ordenação explícita
END;
$$ LANGUAGE plpgsql STABLE;



---------------------------------------------------------------------------
-- Relatório 2 (Lista aeroportos médios e grandes próximos de uma cidade)--
---------------------------------------------------------------------------
--- Índices auxiliares ---
--- Índice que acelera drasticamente a estratégia do bounding box ---
DROP INDEX IF EXISTS idx_aiports_coordinates;
CREATE INDEX idx_airports_coordinates 
ON airports (latitude_deg, longitude_deg);


--- Índice que acelera a busca por nome de cidade (exata) ---
DROP INDEX IF EXISTS idx_cities_name;
CREATE INDEX idx_cities_name
ON cities(name) 
WHERE country_id = 30;

--- Índice que acelera a filtragem por tipo de aeroporto --- 
-- CREATE INDEX idx_airports_type_medium_large 
-- ON airports (airport_type_id) 
-- WHERE airport_type_id IN (4, 7);
-- DROP INDEX IF EXISTS idx_airports_type_medium_large;
    ---Este índice por algum motivo trouxe perda de performance e não ganho, removemos ele

CREATE OR REPLACE FUNCTION get_airport_report_by_city(p_city_name TEXT)
RETURNS TABLE(
    cidade_pesquisada TEXT,
    codigo_iata VARCHAR,
    nome_aeroporto TEXT,
    cidade_aeroporto TEXT,
    distancia_km NUMERIC,
    tipo_aeroporto TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.name::TEXT AS cidade_pesquisada,
        a.iata_code::VARCHAR AS codigo_iata,
        a.name::TEXT AS nome_aeroporto,
        ac.name::TEXT AS cidade_aeroporto,
        -- Cálculo de Haversine protegido contra estouro de precisão decimal
        ROUND((6371 * acos(LEAST(GREATEST(
            cos(radians(c.latitude)) * cos(radians(a.latitude_deg)) * cos(radians(a.longitude_deg) - radians(c.longitude)) + 
            sin(radians(c.latitude)) * sin(radians(a.latitude_deg))
        , -1), 1)))::NUMERIC, 2) AS distancia_km,
        CASE a.airport_type_id 
            WHEN 4 THEN 'medium_airport'::TEXT 
            WHEN 7 THEN 'large_airport'::TEXT 
        END AS tipo_aeroporto
    FROM cities c
    JOIN airports a ON 
        -- Usa Bounding Box para acelerar a consulta, filtrando apenas aeroportos que estejam dentro de uma caixa de 0.9 graus de latitude e 1.2 graus de longitude da cidade (aproximadamente 100 km)
        -- antes de calcular a distância exata com Haversine
        a.latitude_deg BETWEEN c.latitude - 0.9 AND c.latitude + 0.9
        AND a.longitude_deg BETWEEN c.longitude - 1.5 AND c.longitude + 1.5
    LEFT JOIN cities ac ON a.city_id = ac.id
    WHERE c.name = p_city_name
      AND c.country_id = 30 -- Filtrando diretamente o Brasil pelo ID
      AND a.airport_type_id IN (4, 7)
      AND (6371 * acos(LEAST(GREATEST(
            cos(radians(c.latitude)) * cos(radians(a.latitude_deg)) * cos(radians(a.longitude_deg) - radians(c.longitude)) + 
            sin(radians(c.latitude)) * sin(radians(a.latitude_deg))
        , -1), 1))) <= 100
    ORDER BY distancia_km ASC;
END;
$$ LANGUAGE plpgsql STABLE;


-- Explain analyze para avaliar a performance do relatório de aeroportos com ou sem índices (deixo comentado para facilitar desenvolvimento --- REMOVER DEPOIS ---) ---
-- EXPLAIN ANALYZE (SELECT 
--         c.name::TEXT AS cidade_pesquisada,
--         a.iata_code::VARCHAR AS codigo_iata,
--         a.name::TEXT AS nome_aeroporto,
--         ac.name::TEXT AS cidade_aeroporto,
--         -- Cálculo de Haversine protegido contra estouro de precisão decimal
--         ROUND((6371 * acos(LEAST(GREATEST(
--             cos(radians(c.latitude)) * cos(radians(a.latitude_deg)) * cos(radians(a.longitude_deg) - radians(c.longitude)) + 
--             sin(radians(c.latitude)) * sin(radians(a.latitude_deg))
--         , -1), 1)))::NUMERIC, 2) AS distancia_km,
--         CASE a.airport_type_id 
--             WHEN 4 THEN 'medium_airport'::TEXT 
--             WHEN 7 THEN 'large_airport'::TEXT 
--         END AS tipo_aeroporto
--     FROM cities c
--     JOIN airports a ON 
--         -- Usa Bounding Box para acelerar a consulta, filtrando apenas aeroportos que estejam dentro de uma caixa de 0.9 graus de latitude e 1.2 graus de longitude da cidade (aproximadamente 100 km)
--         -- antes de calcular a distância exata com Haversine
--         a.latitude_deg BETWEEN c.latitude - 0.9 AND c.latitude + 0.9
--         AND a.longitude_deg BETWEEN c.longitude - 1.2 AND c.longitude + 1.2
--     LEFT JOIN cities ac ON a.city_id = ac.id
--     WHERE c.name = 'Rio de Janeiro'
--       AND c.country_id = 30 -- Filtrando diretamente o Brasil pelo ID
--       AND a.airport_type_id IN (4, 7)
--       AND (6371 * acos(LEAST(GREATEST(
--             cos(radians(c.latitude)) * cos(radians(a.latitude_deg)) * cos(radians(a.longitude_deg) - radians(c.longitude)) + 
--             sin(radians(c.latitude)) * sin(radians(a.latitude_deg))
--         , -1), 1))) <= 100
--     ORDER BY distancia_km ASC)
    --_Os índices utilizados aceleraram a consulta de ~10ms para ~0.2 ms, uma melhoria de 50x na performance

    
---------------------------------------------------------------------------
-- Relatório 3 (Listar escuderias e relatório multinível)--
---------------------------------------------------------------------------
