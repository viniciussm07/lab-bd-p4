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
CREATE OR REPLACE FUNCTION get_latest_season_races()
RETURNS TABLE(race_name VARCHAR, circuit_name VARCHAR, race_date DATE, race_time TIME, recorded_laps INT) AS $$
BEGIN
    RETURN QUERY
    WITH max_season AS (
        SELECT id FROM seasons ORDER BY year DESC LIMIT 1
    )
    SELECT 
        r.name,
        c.name,
        r.date,
        r.time,
        MAX(res.laps)::INT
    FROM races r
    JOIN circuits c ON r.circuit_id = c.id
    LEFT JOIN results res ON r.id = res.race_id
    -- Ajuste aqui: Filtra pela ID da temporada mais recente
    WHERE r.season_id = (SELECT id FROM max_season)
    GROUP BY r.id, r.name, c.name, r.date, r.time, r.round
    ORDER BY r.round;
END;
$$ LANGUAGE plpgsql STABLE;


--- Ranking dos construtores da última temporada ---
CREATE OR REPLACE FUNCTION get_latest_constructor_standings()
RETURNS TABLE(constructor_name VARCHAR, total_points NUMERIC) AS $$
BEGIN
    RETURN QUERY
    WITH max_season AS (
        SELECT MAX(year) AS ultimo_ano FROM races
    )
    SELECT 
        c.name,
        SUM(res.points)::NUMERIC
    FROM results res
    JOIN races r ON res.race_id = r.id
    JOIN constructors c ON res.constructor_id = c.id
    WHERE r.year = (SELECT ultimo_ano FROM max_season)
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
        SELECT MAX(year) AS ultimo_ano FROM races
    )
    SELECT 
        (d.given_name || ' ' || d.family_name)::TEXT,
        SUM(res.points)::NUMERIC
    FROM results res
    JOIN races r ON res.race_id = r.id
    JOIN drivers d ON res.driver_id = d.id
    WHERE r.year = (SELECT ultimo_ano FROM max_season)
    GROUP BY d.id, d.given_name, d.family_name
    ORDER BY SUM(res.points) DESC;
END;
$$ LANGUAGE plpgsql STABLE;