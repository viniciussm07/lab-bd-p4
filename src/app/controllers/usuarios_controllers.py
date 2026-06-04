# chamando a classe UsuariosDAO
from src.app.BD.usuarios_dao import Usuarios_dao
from src.app.utils.security import SecurityManager
from src.config.database import connection_pool
from src.config.app import aplicacao
from flask import redirect, request, session, make_response, jsonify
import jwt
import datetime

class UsuariosControllers:
    def __init__(self):
        """Inicializa o controller com gerenciador de segurança"""
        self.security = SecurityManager(aplicacao.config['SECRET_KEY'])
    
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
                'sub': usuario['userid'],
                'login': usuario['login'],
                'tipo': usuario['tipo'],
                'id_original': usuario['id_original'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2) # Expira em 2h
            }
            
            token = jwt.encode(payload, '123456', algorithm='HS256')

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
