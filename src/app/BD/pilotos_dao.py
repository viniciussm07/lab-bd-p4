class Pilotos_dao:
    def __init__(self, db_pool):
        self._db_pool = db_pool

    def obter_anos_atividade_piloto(self, driver_ref):
        
        # Chamando a função obter_anos_atividade_piloto e selecionando o primeiro_ano e último_ano retornados
        sql = "SELECT primeiro_ano, ultimo_ano FROM obter_anos_atividade_piloto(%s)"
        
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            

            cursor.execute(sql, (driver_ref,))
            resultado = cursor.fetchone()
            
            cursor.close()

            # Se a função retornar os dados, criamos um dicionário com os dados retornados
            if resultado and resultado[0] is not None:
                return {
                    "primeiro_ano": resultado[0],
                    "ultimo_ano": resultado[1]
                }, None
            else:
                return None, "Nenhum dado de atividade encontrado para este piloto."
                
        except Exception as erro:
            print(f"Erro ao buscar anos de atividade: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def obter_estatisticas_piloto(self, driver_ref):
        # Chamando a função obter_estatisticas_piloto e selecionando o ano, circuito, total_pontos, total_vitorias e total_corridas
        sql = "SELECT ano, circuito, total_pontos, total_vitorias, total_corridas FROM obter_estatisticas_piloto(%s)"
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql, (driver_ref,))
            
            # Utilizamos o fetchall() pois são várias linhas retornadas
            resultados = cursor.fetchall()
            cursor.close()

            if resultados:
                # Formatando a lista de dicionários para o JSON
                lista_estatisticas = []
                for linha in resultados:
                    lista_estatisticas.append({
                        "ano": linha[0],
                        "circuito": linha[1],
                        "total_pontos": float(linha[2]) if linha[2] is not None else 0.0,
                        "total_vitorias": linha[3],
                        "total_corridas": linha[4]
                    })
                return lista_estatisticas, None
            else:
                return [], "Nenhum dado estatístico encontrado para este piloto."
                
        except Exception as erro:
            print(f"Erro ao buscar estatísticas: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)
    def obter_relatorio_6_piloto(self, driver_ref):
          # Chamando a função relatorio_pontos_por_ano_piloto e selecionando o ano, total_pontos e corridas_pontuadas
        sql = "SELECT ano, total_pontos, corridas_pontuadas FROM relatorio_pontos_por_ano_piloto(%s)"
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql, (driver_ref,))
            
            # Utilizamos o fetchall() pois são várias linhas retornadas
            resultados = cursor.fetchall()
            cursor.close()

            if resultados:
                # Formatando a lista de dicionários para o JSON
                lista_estatisticas = []
                for linha in resultados:
                    lista_estatisticas.append({
                        "ano": linha[0],
                        "total_pontos": float(linha[1]) if linha[1] is not None else 0.0,
                        "corridas_pontuadas": linha[2]
                    })
                return lista_estatisticas, None
            else:
                return [], "Nenhum dado no relatório encontrado para este piloto."
                
        except Exception as erro:
            print(f"Erro ao buscar relatório do piloto: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def obter_relatorio_7_piloto(self, driver_ref):
          # Chamando a função relatorio_contagem_status_piloto e selecionando as colunas status_nome e total_ocorrencias
        sql = "SELECT status_nome, total_ocorrencias FROM relatorio_contagem_status_piloto(%s)"
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql, (driver_ref,))
            
            # Utilizamos o fetchall() pois são várias linhas retornadas
            resultados = cursor.fetchall()
            cursor.close()

            if resultados:
                # Formatando a lista de dicionários para o JSON
                lista_estatisticas = []
                for linha in resultados:
                    lista_estatisticas.append({
                        "nome": linha[0],
                        "ocorrencias": linha[1],
                    })
                return lista_estatisticas, None
            else:
                return [], "Nenhum dado no relatório encontrado para este piloto."
                
        except Exception as erro:
            print(f"Erro ao buscar relatório do piloto: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)
        
    def obter_nome_escuderia_piloto(self, driver_ref): 
        
        # Chamando uma query simples que vai retornar apenas o nome do piloto e a escuderia da qual ele está vinculado
        # Ordenamos pelo race_id para buscar a escuderia atual a qual o piloto está correndo.
        sql = """SELECT c.name AS nome_escuderia, d.given_name || ' ' || d.family_name AS nome_piloto
                    FROM drivers d
                    JOIN results r ON r.driver_id = d.id
                    JOIN constructors c ON c.id = r.constructor_id
                    WHERE d.driver_ref = %s
                    ORDER BY r.race_id DESC 
                    LIMIT 1;
        """
        
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            

            cursor.execute(sql, (driver_ref,))
            resultado = cursor.fetchone()
            
            cursor.close()

            # Se a função retornar os dados, criamos um dicionário com os dados retornados
            if resultado and resultado[0] is not None:
                return {
                    "nome_escuderia": resultado[0],
                    "nome_piloto": resultado[1]
                }, None
            else:
                return None, "Nenhum dado encontrado para este piloto."
                
        except Exception as erro:
            print(f"Erro ao buscar anos de atividade: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)
