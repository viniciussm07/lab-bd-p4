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