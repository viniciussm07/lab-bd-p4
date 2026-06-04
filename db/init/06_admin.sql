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

