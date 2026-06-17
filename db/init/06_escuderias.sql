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


-- Retorna os dados de um piloto a partir do seu sobrenome, mas apenas se ele já tiver corrido pela escuderia.
CREATE OR REPLACE FUNCTION consultar_piloto_por_sobrenome(
    piloto_sobrenome VARCHAR,
    piloto_constructor_ref VARCHAR
)
RETURNS TABLE (
    nome_completo VARCHAR,
    data_nascimento DATE,
    nacionalidade VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    -- Utilizamos a cláusula DISTINCT porque o piloto pode ter participado de várias corridas 
    -- pela mesma equipe (existem vários registros em "results"). Vamos listar o piloto uma única vez.
    SELECT DISTINCT
        -- Concatena o nome e o sobrenome
        (d.given_name || ' ' || d.family_name)::VARCHAR AS nome_completo,
        d.date_of_birth,
        ct.nationality::VARCHAR AS nacionalidade
    FROM 
        drivers d
    -- JOINs necessários para validar o histórico do piloto (verifica se existem registros de escuderias e pilotos vinculados a um registro de results) com a escuderia logada.
    JOIN results r ON d.id = r.driver_id
    JOIN constructors c ON r.constructor_id = c.id
    -- JOIN para buscar a informação da nacionalidade.
    JOIN countries ct ON d.country_id = ct.id
    WHERE 
        -- Comparamos o family_name e o piloto_sobrenome passados como parâmetro utilizando a função UPPER para ser case-insensitive (avaliar letras maiúsculas e minúsculas)
        -- O uso dos curingas "%" permitem realizar uma busca parcial do sobrenome.
        UPPER(d.family_name) LIKE UPPER(piloto_sobrenome || '%')
        AND c.constructor_ref = piloto_constructor_ref;
END;
$$ LANGUAGE plpgsql;

-- Cria um índice para otimizar as buscas por prefixo no sobrenome do piloto
CREATE INDEX idx_drivers_family_name_prefix 
ON drivers (UPPER(family_name) varchar_pattern_ops);

-- Retorna a quantidade de vitórias de uma determinada escudaria.
CREATE OR REPLACE FUNCTION consultar_quantidade_vitorias_escuderia(
    p_constructor_ref VARCHAR
)
RETURNS TABLE (
    vitorias BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(r.id) AS vitorias
    FROM 
        results r
    JOIN 
        constructors c ON r.constructor_id = c.id
    WHERE 
        -- Filtra apenas os registros em que o piloto da escuderia ficou em 1º lugar
        r.position_order = 1 
        AND c.constructor_ref = p_constructor_ref;
END;
$$ LANGUAGE plpgsql;

-- Retorna a quantidade de pilotos que correram pela escuderia.
CREATE OR REPLACE FUNCTION consultar_quantidade_pilotos_escuderia(
    p_constructor_ref VARCHAR
)
RETURNS TABLE (
    numero_pilotos BIGINT
) AS $$
BEGIN
    RETURN QUERY
    -- Utilizamos a cláusula DISTINCT porque o piloto pode ter participado de várias corridas 
    -- pela mesma equipe (existem vários registros em "results"). Vamos contar cada piloto uma única vez
    SELECT 
        COUNT (DISTINCT r.driver_id) AS numero_pilotos
    FROM 
        constructors c
    JOIN
        results r ON c.id = r.constructor_id
    WHERE 
        c.constructor_ref = p_constructor_ref;

END;
$$ LANGUAGE plpgsql;

-- Retorna o primeiro e último ano de atividade da escuderia (ano do primeiro e último registro da tabela results)
CREATE OR REPLACE FUNCTION obter_anos_atividade_escuderia(p_constructor_ref VARCHAR)
RETURNS TABLE (
    primeiro_ano INT,
    ultimo_ano INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        -- Utilizamos as funções agregadas (MIN e MAX) para pegar o primeiro e último ano
        -- Além disso utilizamos a função EXTRACT para extrair o ano da coluna race_date
        MIN(EXTRACT(YEAR FROM ra.race_date))::INT AS primeiro_ano,
        MAX(EXTRACT(YEAR FROM ra.race_date))::INT AS ultimo_ano
    FROM 
        constructors c
    JOIN 
        results r ON c.id = r.constructor_id
    -- Esse JOIN é necessário, pois não temos a informação de qual a data em que a escuderia participou na tabela results.
    JOIN 
        races ra ON r.race_id = ra.id
    WHERE 
        -- Filtramos pelo constructor_ref passado como parâmetro
        c.constructor_ref = p_constructor_ref;
END;
$$ LANGUAGE plpgsql;

-- Retorna o nome completo dos pilotos e a quantidade de vitórias que cada um obteve
CREATE OR REPLACE FUNCTION relatorio_pilotos_vitorias(
    p_constructor_ref VARCHAR
)
RETURNS TABLE (
    nome_completo VARCHAR,
    quantidade_vitorias BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        -- Concatena o nome e o sobrenome (nome completo)
        (d.given_name || ' ' || d.family_name)::VARCHAR AS nome_completo,
        -- Conta quantas vezes esse piloto aparece no WHERE (quantas vitórias)
        COUNT(r.id) AS quantidade_vitorias
    FROM 
        results r
    JOIN 
        constructors c ON r.constructor_id = c.id
    JOIN 
        drivers d ON r.driver_id = d.id
    WHERE 
        c.constructor_ref = p_constructor_ref
        AND r.position_order = 1
    GROUP BY 
        -- Agrupamos pelo ID do piloto para garantir que pilotos homônimos (pilotos com mesmo nome e sobrenome) não sejam mesclados e pelas colunas de nome e sobrenome
        d.id, d.given_name, d.family_name
    ORDER BY 
        -- Ordena do piloto com mais vitórias para o com menos vitórias
        quantidade_vitorias DESC;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION relatorio_contagem_status_escuderia(p_constructor_ref VARCHAR)
RETURNS TABLE (
    status_nome TEXT,
    total_ocorrencias BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.status, 
        -- Conta a quantidade de resultados por status
        COUNT(r.id)
    FROM 
        results r
    JOIN 
        status s ON r.status_id = s.id
    JOIN 
        constructors c ON r.constructor_id = c.id
    WHERE 
        c.constructor_ref = p_constructor_ref
    -- Agrupando pelo status
    GROUP BY 
        s.status;
END;
$$ LANGUAGE plpgsql;