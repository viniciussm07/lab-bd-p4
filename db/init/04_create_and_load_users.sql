CREATE TABLE USERS (
    userid SERIAL PRIMARY KEY,
    login VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('Admin', 'Escuderia', 'Piloto')),
    id_original VARCHAR(255) -- Fica nulo quando for o usuário Admin
);

CREATE EXTENSION IF NOT EXISTS pgcrypto;

DO $$
DECLARE
    escuderia RECORD;
    piloto RECORD;
BEGIN
    RAISE NOTICE 'Carregando usuario admin...';
    INSERT INTO users (login, password, tipo, id_original)
    VALUES (
        'admin', 
        crypt('admin', gen_salt('bf', 10)), 
        'Admin', 
        NULL
    )
    ON CONFLICT (login) DO NOTHING;

    RAISE NOTICE 'Populando usuarios de escuderias...';
    FOR escuderia IN SELECT constructor_ref FROM constructors 
    LOOP
        INSERT INTO users (login, password, tipo, id_original)
        VALUES (
            escuderia.constructor_ref || '_c', 
            crypt(escuderia.constructor_ref, gen_salt('bf', 10)), 
            'Escuderia', 
            escuderia.constructor_ref
        )
        ON CONFLICT (login) DO NOTHING;
    END LOOP;

    RAISE NOTICE 'Populando usuarios pilotos...';
    FOR piloto IN SELECT driver_ref FROM drivers 
    LOOP
        INSERT INTO users (login, password, tipo, id_original)
        VALUES (
            piloto.driver_ref || '_d', 
            crypt(piloto.driver_ref, gen_salt('bf', 10)), 
            'Piloto', 
            piloto.driver_ref
        )
        ON CONFLICT (login) DO NOTHING;
    END LOOP;

    RAISE NOTICE 'Finalizado: carga de usuarios concluida.';
    
EXCEPTION WHEN OTHERS THEN
    RAISE EXCEPTION 'Erro durante a execução da população dos usuários: %', SQLERRM;
END $$;