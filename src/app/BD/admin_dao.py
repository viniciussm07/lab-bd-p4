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

    def obter_relatorio_contagem_status(self):
        sql = "SELECT status, count FROM get_result_status_counts()"
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            cursor.close()

            return [
                {"status": linha[0], "contagem": linha[1]}
                for linha in resultados
            ], None

        except Exception as erro:
            print(f"Erro ao buscar relatório de status: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def obter_relatorio_aeroportos(self, cidade):
        sql = (
            "SELECT cidade_pesquisada, codigo_iata, nome_aeroporto, cidade_aeroporto, "
            "distancia_km, tipo_aeroporto FROM get_airport_report_by_city(%s)"
        )
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql, (cidade,))
            resultados = cursor.fetchall()
            cursor.close()

            return [
                {
                    "cidade_pesquisada": linha[0],
                    "codigo_iata": linha[1],
                    "nome_aeroporto": linha[2],
                    "cidade_aeroporto": linha[3],
                    "distancia_km": float(linha[4]) if linha[4] is not None else 0.0,
                    "tipo_aeroporto": linha[5],
                }
                for linha in resultados
            ], None

        except Exception as erro:
            print(f"Erro ao buscar relatório de aeroportos: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def obter_relatorio_escuderias_pilotos(self):
        sql = "SELECT constructor_name, driver_count FROM get_admin_report_constructors()"
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            cursor.close()

            return [
                {
                    "nome_escuderia": linha[0],
                    "quantidade_pilotos": linha[1],
                }
                for linha in resultados
            ], None

        except Exception as erro:
            print(f"Erro ao buscar relatório de escuderias: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def obter_relatorio_total_corridas(self):
        sql = "SELECT total_races FROM get_admin_report_total_races()"
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql)
            resultado = cursor.fetchone()
            cursor.close()

            if not resultado:
                return {"total_corridas": 0}, None

            return {"total_corridas": resultado[0]}, None

        except Exception as erro:
            print(f"Erro ao buscar total de corridas: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def obter_relatorio_circuitos(self):
        sql = (
            "SELECT circuit_id, circuit_name, race_count, min_laps, avg_laps, max_laps "
            "FROM get_admin_report_circuits()"
        )
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            cursor.close()

            return [
                {
                    "circuito_id": linha[0],
                    "nome_circuito": linha[1],
                    "quantidade_corridas": linha[2],
                    "voltas_minimas": linha[3],
                    "voltas_medias": float(linha[4]) if linha[4] is not None else 0.0,
                    "voltas_maximas": linha[5],
                }
                for linha in resultados
            ], None

        except Exception as erro:
            print(f"Erro ao buscar relatório de circuitos: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def obter_relatorio_corridas_por_circuito(self, circuit_id):
        sql = (
            "SELECT race_name, race_date, recorded_laps, participating_drivers "
            "FROM get_report_races_by_circuit(%s)"
        )
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql, (circuit_id,))
            resultados = cursor.fetchall()
            cursor.close()

            return [
                {
                    "nome_corrida": linha[0],
                    "data": linha[1].strftime("%Y-%m-%d") if linha[1] else None,
                    "voltas_registradas": linha[2] if linha[2] is not None else 0,
                    "pilotos_participantes": linha[3],
                }
                for linha in resultados
            ], None

        except Exception as erro:
            print(f"Erro ao buscar corridas do circuito: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def cadastrar_escuderia(self, constructor_ref, name, country_id, wikipedia_url):
        sql = """
            INSERT INTO constructors (constructor_ref, name, country_id, wikipedia_url)
            VALUES (%s, %s, %s, %s)
            RETURNING id, constructor_ref, name, country_id, wikipedia_url
        """
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (constructor_ref, name, country_id, wikipedia_url or None),
            )
            linha = cursor.fetchone()
            conn.commit()
            cursor.close()

            return {
                "mensagem": "Escuderia cadastrada com sucesso.",
                "escuderia": {
                    "id": linha[0],
                    "constructor_ref": linha[1],
                    "name": linha[2],
                    "country_id": linha[3],
                    "wikipedia_url": linha[4],
                    "login_gerado": f"{linha[1]}_c",
                },
            }, None

        except Exception as erro:
            if conn:
                conn.rollback()
            print(f"Erro ao cadastrar escuderia: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def cadastrar_piloto(self, driver_ref, given_name, family_name, date_of_birth, country_id):
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(
                "CALL inserir_piloto_arquivo(%s, %s, %s, %s, %s)",
                (driver_ref, given_name, family_name, date_of_birth, country_id),
            )
            cursor.execute(
                """
                SELECT id, driver_ref, given_name, family_name, date_of_birth, country_id
                FROM drivers
                WHERE driver_ref = %s
                """,
                (driver_ref,),
            )
            linha = cursor.fetchone()
            conn.commit()
            cursor.close()

            if not linha:
                return None, "Piloto inserido, mas não foi possível recuperar os dados."

            return {
                "mensagem": "Piloto cadastrado com sucesso.",
                "piloto": {
                    "id": linha[0],
                    "driver_ref": linha[1],
                    "given_name": linha[2],
                    "family_name": linha[3],
                    "date_of_birth": linha[4].strftime("%Y-%m-%d") if linha[4] else None,
                    "country_id": linha[5],
                    "login_gerado": f"{linha[1]}_d",
                },
            }, None

        except Exception as erro:
            if conn:
                conn.rollback()
            print(f"Erro ao cadastrar piloto: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)
