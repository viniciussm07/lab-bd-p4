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