# chamando a classe usuarios_controller
from src.app.controllers.usuarios_controllers import UsuariosControllers
from src.app.controllers.pilotos_controllers import PilotosControllers
from src.app.middlewares.auth_middleware import auth_middleware
usuario_cont = UsuariosControllers()
piloto_cont = PilotosControllers()

def rotas(aplicacao):
    # Evitar problema com o CORS
    @aplicacao.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Origin'] = "http://localhost"
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    @aplicacao.route('/api/login', methods=['POST'])
    def login():
        return usuario_cont.api_login()
        
    @aplicacao.route('/api/piloto/anos-atividade', methods=['GET'])
    @auth_middleware(tipo_permitido="Piloto")
    def obter_anos_atividade_piloto(usuario_logado):
        # Extraimos o driver_ref que é o id_original presente no token
        driver_ref = usuario_logado.get('id_original')
        
        return piloto_cont.api_obter_anos_atividade_piloto(driver_ref)
    

