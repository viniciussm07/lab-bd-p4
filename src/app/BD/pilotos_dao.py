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