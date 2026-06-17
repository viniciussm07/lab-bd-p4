class Admin_dao:
    def __init__(self, db_pool):
        self._db_pool = db_pool

    def obter_resumo(self):
        sql = "SELECT total_drivers, total_constructors, total_seasons FROM get_db_summary()"
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql)
            resultado = cursor.fetchone()
            cursor.close()

            if not resultado:
                return None, "Nenhum dado de resumo encontrado."

            return {
                "total_pilotos": resultado[0],
                "total_escuderias": resultado[1],
                "total_temporadas": resultado[2],
            }, None

        except Exception as erro:
            print(f"Erro ao buscar resumo do dashboard admin: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def obter_corridas_ultima_temporada(self):
        sql = (
            "SELECT race_name, circuit_name, race_date, race_time, recorded_laps "
            "FROM get_latest_season_races()"
        )
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            cursor.close()

            corridas = []
            for linha in resultados:
                corridas.append({
                    "nome_corrida": linha[0],
                    "circuito": linha[1],
                    "data": linha[2].strftime("%Y-%m-%d") if linha[2] else None,
                    "horario": linha[3].strftime("%H:%M:%S") if linha[3] else None,
                    "voltas_registradas": linha[4] if linha[4] is not None else 0,
                })

            return corridas, None

        except Exception as erro:
            print(f"Erro ao buscar corridas da última temporada: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def obter_ranking_escuderias(self):
        sql = (
            "SELECT constructor_name, total_points "
            "FROM get_latest_constructor_standings_from_standings()"
        )
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            cursor.close()

            ranking = []
            for linha in resultados:
                ranking.append({
                    "nome_escuderia": linha[0],
                    "total_pontos": float(linha[1]) if linha[1] is not None else 0.0,
                })

            return ranking, None

        except Exception as erro:
            print(f"Erro ao buscar ranking de escuderias: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def obter_ranking_pilotos(self):
        sql = (
            "SELECT driver_name, total_points "
            "FROM get_latest_driver_standings_from_standings()"
        )
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            cursor.close()

            ranking = []
            for linha in resultados:
                ranking.append({
                    "nome_piloto": linha[0],
                    "total_pontos": float(linha[1]) if linha[1] is not None else 0.0,
                })

            return ranking, None

        except Exception as erro:
            print(f"Erro ao buscar ranking de pilotos: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)
