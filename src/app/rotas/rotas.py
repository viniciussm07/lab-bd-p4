# chamando a classe usuarios_controller
from src.app.controllers.usuarios_controllers import UsuariosControllers
from src.app.controllers.pilotos_controllers import PilotosControllers
from src.app.controllers.escuderias_controllers import EscuderiaControllers
from src.app.middlewares.auth_middleware import auth_middleware
from flask import request, render_template
usuario_cont = UsuariosControllers()
piloto_cont = PilotosControllers()
escuderia_cont = EscuderiaControllers()

def rotas(aplicacao):
    # Evitar problema com o CORS
    @aplicacao.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Origin'] = "http://127.0.0.1:5500"
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers["Access-Control-Allow-Credentials"] = "true"
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
    
    @aplicacao.route('/api/piloto/estatisticas', methods=['GET'])
    @auth_middleware(tipo_permitido="Piloto")
    def obter_estatisticas_piloto(usuario_logado):
        # Extraimos o driver_ref que é o id_original presente no token
        driver_ref = usuario_logado.get('id_original')
        
        return piloto_cont.api_obter_estatisticas_piloto(driver_ref)
    
    @aplicacao.route('/api/piloto/relatorio-pontos-ano', methods=['GET'])
    @auth_middleware(tipo_permitido="Piloto")
    def obter_relatorio_6_piloto(usuario_logado):
        # Extraimos o driver_ref que é o id_original presente no token
        driver_ref = usuario_logado.get('id_original')
        
        return piloto_cont.api_obter_relatorio_6_piloto(driver_ref)
    
    @aplicacao.route('/api/piloto/relatorio-contagem-status', methods=['GET'])
    @auth_middleware(tipo_permitido="Piloto")
    def obter_relatorio_7_piloto(usuario_logado):
        # Extraimos o driver_ref que é o id_original presente no token
        driver_ref = usuario_logado.get('id_original')
        
        return piloto_cont.api_obter_relatorio_7_piloto(driver_ref)
    
    @aplicacao.route('/api/escuderia/piloto-arquivo', methods=['POST'])
    @auth_middleware(tipo_permitido="Escuderia")
    def inserir_piloto_arquivo_escuderia(usuario_logado):
        # Obtendo o arquivo enviado na rota
        arquivo = request.files.get('file') 
        return escuderia_cont.api_inserir_escuderia_arquivo(arquivo)
    
    @aplicacao.route('/api/escuderia/piloto-sobrenome', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def consultar_piloto_sobrenome_escuderia(usuario_logado):
        # Obtendo o sobrenome enviado como parâmetro na URL (ex: ?sobrenome=Senna)
        sobrenome = request.args.get('sobrenome')
        
        # Obtendo o identificador da escuderia logada
        constructor_ref = usuario_logado.get('id_original')
        
        return escuderia_cont.api_consultar_piloto_por_sobrenome(sobrenome, constructor_ref)
    
    @aplicacao.route('/api/escuderia/vitorias', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def consultar_quantidade_vitorias_escuderia(usuario_logado):
        # Obtendo o identificador da escuderia logada
        constructor_ref = usuario_logado.get('id_original')

        return escuderia_cont.api_consultar_quantidade_vitorias_escuderia(constructor_ref)
    
    @aplicacao.route('/api/escuderia/quantidade-pilotos', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def consultar_quantidade_pilotos_escuderia(usuario_logado):
        # Obtendo o identificador da escuderia logada
        constructor_ref = usuario_logado.get('id_original')
        
        return escuderia_cont.api_consultar_quantidade_pilotos_escuderia(constructor_ref)
    
    @aplicacao.route('/api/escuderia/anos-atividade', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def obter_anos_atividade_escuderia(usuario_logado):
        # Obtendo o identificador da escuderia logada
        constructor_ref = usuario_logado.get('id_original')
        
        return escuderia_cont.api_obter_anos_atividade_escuderia(constructor_ref)
    
    @aplicacao.route('/api/escuderia/relatorio-pilotos-vitorias', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def obter_relatorio_4_escuderia(usuario_logado):
        # Obtendo o identificador da escuderia logada
        constructor_ref = usuario_logado.get('id_original')
        
        return escuderia_cont.api_obter_relatorio_4_escuderia(constructor_ref)  
    
    @aplicacao.route('/api/escuderia/relatorio-contagem-status', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def obter_relatorio_5_escuderia(usuario_logado):
        # Obtendo o identificador da escuderia logada
        constructor_ref = usuario_logado.get('id_original')
        
        return escuderia_cont.api_obter_relatorio_5_escuderia(constructor_ref)
    
    # Rotas comuns da API a todos os tipos de usuários
    @aplicacao.route('/api/me', methods=['GET'])
    @auth_middleware(tipo_permitido=["Piloto", "Escuderia", "Admin"])
    def obter_nome_escuderia_piloto(usuario_logado):
        tipo = usuario_logado.get('tipo')
        driver_ref = usuario_logado.get('id_original')
        if tipo == 'Piloto':
            return piloto_cont.api_obter_nome_escuderia_piloto(driver_ref)

    # Views/Telas
    @aplicacao.route('/dashboard', methods=['GET'])
    @auth_middleware(tipo_permitido=["Piloto", "Escuderia", "Admin"])
    def view_dashboard(usuario_logado):
        tipo = usuario_logado.get('tipo')
        if tipo == 'Piloto':
            return render_template('dashboard_piloto.html')

    

    

