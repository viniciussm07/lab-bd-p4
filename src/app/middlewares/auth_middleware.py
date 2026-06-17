from functools import wraps
from flask import request, jsonify
import jwt

def auth_middleware(tipo_permitido=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Pegamos o token de autenticação
            token = request.cookies.get('auth_token')
            print(token)

            # Se o token não existir retornamos uma mensagem de erro e um status 401 (Unauthorized)
            if not token:
                return jsonify({"erro": "Acesso não autorizado. Faça login para continuar."}), 401
            
            try:
                secret_key = "123456"
                
                # Decodificamos o token
                payload = jwt.decode(token, secret_key, algorithms=["HS256"])
                print(payload)
                # Caso tipo_permitido seja uma lista, então verificamos se o tipo do usuário é compátivel com algum tipo passado na lista.
                if isinstance(tipo_permitido, list):
                    if payload.get('tipo') not in tipo_permitido:
                        return jsonify({"erro": f"Acesso negado. Rota exclusiva para {tipo_permitido}."}), 403
                # Verificamos se o tipo extraído do token é de fato um Piloto, se não for retornamos um erro e um status 403 (Forbidden)
                elif tipo_permitido and payload.get('tipo') != tipo_permitido:
                    return jsonify({"erro": f"Acesso negado. Rota exclusiva para {tipo_permitido}."}), 403

                kwargs['usuario_logado'] = payload

            except jwt.ExpiredSignatureError:
                # Se o error for relacionado a expiração do token retornamos um erro com o status 401 (Unauthorized)
                return jsonify({"erro": "Sessão expirada. Faça login novamente."}), 401
            except jwt.InvalidTokenError as e:
                print(e)
                # Se o error for relacionado a validade do token retornamos um erro com o status 401 (Unauthorized)
                return jsonify({"erro": "Token inválido. Acesso negado."}), 401

            return f(*args, **kwargs)
        return decorated_function
    return decorator