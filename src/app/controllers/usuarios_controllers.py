# chamando a classe UsuariosDAO
from src.app.BD.usuarios_dao import Usuarios_dao
from src.config.database import connection_pool
from flask import request, make_response, jsonify
import jwt
import datetime

class UsuariosControllers:
    def __init__(self):
        """Inicializa o controller com gerenciador de segurança"""    
    def api_login(self):
            dados = request.get_json()
            print(dados)
            
            if not dados or not dados.get('login') or not dados.get('password'):
                return jsonify({"erro": "Login e senha são obrigatórios"}), 400

            login_informado = dados.get('login')
            senha_informada = dados.get('password')

            usuario_dao = Usuarios_dao(connection_pool)
            usuario, erro = usuario_dao.autenticar_usuario_f1(login_informado, senha_informada)

            if erro:
                status_code = 500 if erro == "Erro interno no servidor" else 401
                return jsonify({"erro": erro}), status_code

            payload = {
                 # Como sub deve ser do tipo str e userid é um campo do tipo int, precisamos converter ele para str 
                'sub': str(usuario['userid']),
                'login': usuario['login'],
                'tipo': usuario['tipo'],
                'id_original': usuario['id_original'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2) # Expira em 2h
            }
            secret_key = "123456"
            
            token = jwt.encode(payload, secret_key, algorithm="HS256")


            resposta = make_response(jsonify({
                "mensagem": "Login efetuado com sucesso!",
                "tipo": usuario['tipo']
            }))

            resposta.set_cookie(
                'auth_token',
                token,
                httponly=True,
                secure=False, 
                max_age=2 * 60 * 60
            )

            return resposta, 200
    def api_logout(self):
        token = request.cookies.get('auth_token')
        if token:
            try:
                payload = jwt.decode(token, "123456", algorithms=["HS256"])
                # Conversão explícita para int, já que o "sub" foi salvo como string no login
                userid = int(payload['sub']) 
                usuario_dao = Usuarios_dao(connection_pool)
                usuario_dao.registrar_log_logout(userid)
            except Exception as e:
                print(f"Erro ao registrar logout: {e}")

        resposta = make_response(jsonify({"mensagem": "Logout realizado com sucesso"}))
        resposta.set_cookie('auth_token', '', expires=0)
        return resposta, 200