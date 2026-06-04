# chamando a classe usuarios_controller
from src.app.controllers.usuarios_controllers import UsuariosControllers

usuario_cont = UsuariosControllers()

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
