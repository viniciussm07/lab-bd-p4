-- Funções referentes ao Piloto --.

CREATE OR REPLACE FUNCTION obter_anos_atividade_piloto(p_driver_ref VARCHAR)
RETURNS TABLE (
    -- Declaração das variáveis de retorno (primeiro e último ano)
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
        drivers d
    JOIN 
        results r ON d.id = r.driver_id
    -- Esse JOIN é necessário, pois não temos a informação de qual a data em que o piloto correu na tabela results.
    JOIN 
        races ra ON r.race_id = ra.id
    WHERE 
        -- Filtramos pelo driver_ref passado como parâmetro
        d.driver_ref = p_driver_ref;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION obter_estatisticas_piloto(p_driver_ref VARCHAR)
RETURNS TABLE (
    -- Declaração das variáveis de retorno: ano (ano da corrida), circuito (nome do circuito), total_pontos (quantidade total de pontos obtidos pelo piloto), total_vitorias (número de vítorias do piloto), total_corridas (total de corridas realizadas pelo piloto)
    ano INT,
    circuito VARCHAR,
    total_pontos NUMERIC,
    total_vitorias INT,
    total_corridas INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        -- Utilizamos a função EXTRACT para extrair o ano da coluna race_date
        EXTRACT(YEAR FROM ra.race_date)::INT AS ano,
            c.name::VARCHAR AS circuito,
        -- Somamos todos os pontos da tabela results
        SUM(r.points) AS total_pontos,
        -- Aqui realizamos uma contagem do número de vitórias, caso a position_order seja = 1, acrescentamos o valor 1 ao total, senão ignoramos.
        COUNT(CASE WHEN r.position_order = 1 THEN 1 END)::INT AS total_vitorias,
        COUNT(r.id)::INT AS total_corridas
    FROM 
        drivers d
    JOIN 
        results r ON d.id = r.driver_id
    JOIN 
        races ra ON r.race_id = ra.id
    JOIN 
        circuits c ON ra.circuit_id = c.id
    WHERE 
        d.driver_ref = p_driver_ref
    -- Aqui realizamos o agrupando pelo ano que a corrida ocorreu e pelo nome do circuito
    GROUP BY 
        ano, 
        c.name
    -- Ordenamos o resultado por ano e pelo total de pontos
    ORDER BY 
        ano DESC, 
        total_pontos DESC;
END;
$$ LANGUAGE plpgsql;