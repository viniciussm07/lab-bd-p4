import bcrypt

class Usuarios_dao:
    def __init__(self, db_pool):
        self._db_pool = db_pool
        # Inicializa o gerenciador de segurança

    def autenticar_usuario_f1(self, login, senha):
        """
        Valida se existe um usuário cadastrado no banco de dados que tem as credenciais passadas como parâmetro.
        """

        sql_cons_usuarios = """
            SELECT userid, login, tipo, password, id_original
            FROM users
            WHERE login = %s
        """

        # sql_log = """
        #     INSERT INTO USERS_LOG (userid, acao) VALUES (%s, 'LOGIN')
        # """

        conn = None
        
        try:
            conn = self._db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(sql_cons_usuarios, (login,))
            resultado = cursor.fetchone()

            # Verificando se existe o usuário
            if resultado:
                colunas = ["userid", "login", "tipo", "password", "id_original"]
                usuario = dict(zip(colunas, resultado))

                senha_hash = usuario['password']
                if verify_password(senha, senha_hash):

                    # cursor.execute(sql_log, (usuario['userid'],))
                    conn.commit()

                    usuario.pop('password', None)
                    return usuario, None
                else:
                    return None, "Credenciais inválidas"
            else:
                return None, "Credenciais inválidas"
        except Exception as erro:
            if conn:
                conn.rollback()
            print(f"Erro ao autenticar: {erro}")
            return None, "Erro interno no servidor"
        finally:
            if conn:
                cursor.close()
                self._db_pool.putconn(conn)
        

def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha corresponde ao hash
        
        Args:
            password: Senha em texto plano
            hashed_password: Hash armazenado no banco
            
        Returns:
            True se a senha corresponde, False caso contrário
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            print(f"Erro ao verificar senha: {e}")
            return False