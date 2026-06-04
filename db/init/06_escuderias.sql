-- Funções referentes a Escuderia --.

CREATE OR REPLACE PROCEDURE inserir_piloto_arquivo(
    p_ref VARCHAR, p_given VARCHAR, p_family VARCHAR, p_dob DATE, p_country INT
)
LANGUAGE plpgsql AS $$
BEGIN
    -- Aqui verificamos se já existe um piloto com o mesmo nome e sobrenome conforme exigido no pdf, se existir é lançada uma exceção.
    IF EXISTS (SELECT 1 FROM drivers WHERE given_name = p_given AND family_name = p_family) THEN
        RAISE EXCEPTION 'Piloto % % já cadastrado', p_given, p_family;
    END IF;

    -- Se não existir um piloto com o mesmo nome e sobrenome, então inserimos
    INSERT INTO drivers (driver_ref, given_name, family_name, date_of_birth, country_id)
    VALUES (p_ref, p_given, p_family, p_dob, p_country);
END;
$$;