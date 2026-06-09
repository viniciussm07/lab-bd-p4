import io
import csv

class Escuderias_dao:
    def __init__(self, db_pool):
        self._db_pool = db_pool

    def inserir_escuderia_arquivo(self, arquivo):
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            
            # Lê e decodifica o arquivo enviado
            stream = io.StringIO(arquivo.stream.read().decode("UTF8"), newline=None)
            reader = csv.reader(stream)
            
            # Utilizamos essa variável para armazenar a quantidade de registros que são válidos
            sucessos = 0

            # Utilizamos essa variável para armazenar os erros para informar detalhadamente qual a linha que os dados estão mal formatados ou se já existe na base de dados
            erros = []

            for linha in reader:
                try:
                    # Executa a Procedure inserir_piloto_arquivo
                    cursor.execute("CALL inserir_piloto_arquivo(%s, %s, %s, %s, %s)", 
                                   (linha[0], linha[1], linha[2], linha[3], linha[4]))
                    # Se inserirmos os dados da linha na tabela (não houver nenhum erro) incrementamos a variável sucessos
                    sucessos += 1
                except Exception as e:
                    # Aqui adicionamos os logs dos erros, dizemos em qual linha ocorreu seguido por : tipo de erro
                    erros.append(f"Erro na linha {linha[0]}: {str(e)}")
            
            conn.commit()
            cursor.close()
            
            # Segue o padrão de retorno (dados, erro)
            return {"sucessos": sucessos, "erros": erros}, None

        except Exception as erro:
            if conn: conn.rollback()
            print(f"Erro no processamento do arquivo: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)

    def consultar_piloto_por_sobrenome(self, sobrenome, constructor_ref):
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            
            # Executa a função consultar_piloto_por_sobrenome e retorna as colunas nome_completo, data_nascimento e nacionalidade 
            cursor.execute(
                "SELECT nome_completo, data_nascimento, nacionalidade FROM consultar_piloto_por_sobrenome(%s, %s);",
                (sobrenome, constructor_ref)
            )
            
            resultados = cursor.fetchall()
            
            # Se não encontrar nenhuma tupla então retorna uma lista vazia sem erro (None)
            if not resultados:
                return [], None

            # Formata os dados retornados do banco para uma lista de dicionários
            pilotos = []
            for linha in resultados:
                pilotos.append({
                    "nome_completo": linha[0],
                    # Converte a data para string (formato ISO) para evitar problemas no JSON do Flask
                    "data_nascimento": linha[1].strftime('%Y-%m-%d') if linha[1] else None,
                    "nacionalidade": linha[2]
                })
            
            cursor.close()
            
            # Segue o padrão de retorno (dados, erro)
            return pilotos, None

        except Exception as erro:
            print(f"Erro ao consultar piloto por sobrenome: {erro}")
            return None, "Erro interno no servidor ao realizar a consulta."
        finally:
            if conn:
                self._db_pool.putconn(conn)
    def consultar_quantidade_vitorias_escuderia(self, constructor_ref):
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            
            # Executa a função consultar_quantidade_vitorias_escuderia e retorna a quantidade de vitórias
            cursor.execute(
                "SELECT vitorias FROM consultar_quantidade_vitorias_escuderia(%s);",
                (constructor_ref,)
            )
            
            resultado = cursor.fetchone()

            # Se não encontrar nenhuma tupla então retorna um dicionário com o número de vitórias e sem erro (None)
            if not resultado:
                return {"vitorias": 0}, None

            dados = {"vitorias": resultado[0]}
            
            cursor.close()

            # Segue o padrão de retorno (dados, erro)
            return dados, None

        except Exception as erro:
            print(f"Erro ao consultar quantidade de vitórias da escuderia: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)
                
    def consultar_quantidade_pilotos_escuderia(self, constructor_ref):
        conn = None
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            
            # Executa a função consultar_quantidade_pilotos_escuderia e retorna a quantidade de pilotos
            cursor.execute(
                "SELECT numero_pilotos FROM consultar_quantidade_pilotos_escuderia(%s);",
                (constructor_ref,)
            )
            
            resultado = cursor.fetchone()

            # Se não encontrar nenhuma tupla então retorna um dicionário com o número de pilotos zerado e sem erro (None)
            if not resultado:
                return {"numero_pilotos": 0}, None

            dados = {"numero_pilotos": resultado[0]}
            
            cursor.close()

            # Segue o padrão de retorno (dados, erro)
            return dados, None

        except Exception as erro:
            print(f"Erro ao consultar a quantidade de pilotos da escuderia: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                self._db_pool.putconn(conn)