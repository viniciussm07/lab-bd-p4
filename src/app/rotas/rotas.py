# chamando as classes dos controllers
from src.app.controllers.usuarios_controllers import UsuariosControllers
from src.app.controllers.pilotos_controllers import PilotosControllers
from src.app.controllers.escuderias_controllers import EscuderiaControllers
from src.app.controllers.admin_controllers import AdminControllers
from src.app.middlewares.auth_middleware import auth_middleware
from flask import request, render_template, jsonify

usuario_cont = UsuariosControllers()
piloto_cont = PilotosControllers()
escuderia_cont = EscuderiaControllers()
admin_cont = AdminControllers()

def rotas(aplicacao):
    # Evitar problema com o CORS
    @aplicacao.after_request
    def after_request(response):
        # Configurado para aceitar requisições do seu Live Server local
        response.headers['Access-Control-Allow-Origin'] = "http://127.0.0.1:5500"
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    # --- Autenticação ---
    @aplicacao.route('/api/login', methods=['POST'])
    def login():
        return usuario_cont.api_login()
    
    @aplicacao.route('/api/logout', methods=['POST'])
    def logout():
        return usuario_cont.api_logout()
        
    # --- Rotas de Pilotos ---
    @aplicacao.route('/api/piloto/anos-atividade', methods=['GET'])
    @auth_middleware(tipo_permitido="Piloto")
    def obter_anos_atividade_piloto(usuario_logado):
        driver_ref = usuario_logado.get('id_original')
        return piloto_cont.api_obter_anos_atividade_piloto(driver_ref)
    
    @aplicacao.route('/api/piloto/estatisticas', methods=['GET'])
    @auth_middleware(tipo_permitido="Piloto")
    def obter_estatisticas_piloto(usuario_logado):
        driver_ref = usuario_logado.get('id_original')
        return piloto_cont.api_obter_estatisticas_piloto(driver_ref)
    
    @aplicacao.route('/api/piloto/relatorio-pontos-ano', methods=['GET'])
    @auth_middleware(tipo_permitido="Piloto")
    def obter_relatorio_6_piloto(usuario_logado):
        driver_ref = usuario_logado.get('id_original')
        return piloto_cont.api_obter_relatorio_6_piloto(driver_ref)
    
    @aplicacao.route('/api/piloto/relatorio-contagem-status', methods=['GET'])
    @auth_middleware(tipo_permitido="Piloto")
    def obter_relatorio_7_piloto(usuario_logado):
        driver_ref = usuario_logado.get('id_original')
        return piloto_cont.api_obter_relatorio_7_piloto(driver_ref)
    
    # --- Rotas de Escuderias ---
    @aplicacao.route('/api/escuderia/piloto-arquivo', methods=['POST'])
    @auth_middleware(tipo_permitido="Escuderia")
    def inserir_piloto_arquivo_escuderia(usuario_logado):
        arquivo = request.files.get('file') 
        return escuderia_cont.api_inserir_escuderia_arquivo(arquivo)
    
    @aplicacao.route('/api/escuderia/piloto-sobrenome', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def consultar_piloto_sobrenome_escuderia(usuario_logado):
        sobrenome = request.args.get('sobrenome')
        constructor_ref = usuario_logado.get('id_original')
        return escuderia_cont.api_consultar_piloto_por_sobrenome(sobrenome, constructor_ref)
    
    @aplicacao.route('/api/escuderia/vitorias', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def consultar_quantidade_vitorias_escuderia(usuario_logado):
        constructor_ref = usuario_logado.get('id_original')
        return escuderia_cont.api_consultar_quantidade_vitorias_escuderia(constructor_ref)
    
    @aplicacao.route('/api/escuderia/quantidade-pilotos', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def consultar_quantidade_pilotos_escuderia(usuario_logado):
        constructor_ref = usuario_logado.get('id_original')
        return escuderia_cont.api_consultar_quantidade_pilotos_escuderia(constructor_ref)
    
    @aplicacao.route('/api/escuderia/anos-atividade', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def obter_anos_atividade_escuderia(usuario_logado):
        constructor_ref = usuario_logado.get('id_original')
        return escuderia_cont.api_obter_anos_atividade_escuderia(constructor_ref)
    
    @aplicacao.route('/api/escuderia/relatorio-pilotos-vitorias', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def obter_relatorio_4_escuderia(usuario_logado):
        constructor_ref = usuario_logado.get('id_original')
        return escuderia_cont.api_obter_relatorio_4_escuderia(constructor_ref)  
    
    @aplicacao.route('/api/escuderia/relatorio-contagem-status', methods=['GET'])
    @auth_middleware(tipo_permitido="Escuderia")
    def obter_relatorio_5_escuderia(usuario_logado):
        constructor_ref = usuario_logado.get('id_original')
        return escuderia_cont.api_obter_relatorio_5_escuderia(constructor_ref)
    
    # --- Rotas de Admin (Dashboard) ---
    @aplicacao.route('/api/admin/resumo', methods=['GET'])
    @auth_middleware(tipo_permitido="Admin")
    def obter_resumo_admin(usuario_logado):
        return admin_cont.api_obter_resumo()

    @aplicacao.route('/api/admin/corridas-ultima-temporada', methods=['GET'])
    @auth_middleware(tipo_permitido="Admin")
    def obter_corridas_ultima_temporada_admin(usuario_logado):
        return admin_cont.api_obter_corridas_ultima_temporada()

    @aplicacao.route('/api/admin/ranking-escuderias', methods=['GET'])
    @auth_middleware(tipo_permitido="Admin")
    def obter_ranking_escuderias_admin(usuario_logado):
        return admin_cont.api_obter_ranking_escuderias()

    @aplicacao.route('/api/admin/ranking-pilotos', methods=['GET'])
    @auth_middleware(tipo_permitido="Admin")
    def obter_ranking_pilotos_admin(usuario_logado):
        return admin_cont.api_obter_ranking_pilotos()

    # --- Perfil Comum ---
    @aplicacao.route('/api/me', methods=['GET'])
    @auth_middleware(tipo_permitido=["Piloto", "Escuderia", "Admin"])
    def obter_perfil_usuario(usuario_logado):
        tipo = usuario_logado.get('tipo')
        id_original = usuario_logado.get('id_original')
        
        if tipo == 'Piloto':
            return piloto_cont.api_obter_nome_escuderia_piloto(id_original)
        elif tipo == 'Escuderia':
            return escuderia_cont.api_obter_nome_escuderia(id_original)
        elif tipo == 'Admin':
            return jsonify({"nome_escuderia": "Administrador do Sistema"}), 200

    # --- Views/Telas ---
    @aplicacao.route('/dashboard', methods=['GET'])
    @auth_middleware(tipo_permitido=["Piloto", "Escuderia", "Admin"])
    def view_dashboard(usuario_logado):
        tipo = usuario_logado.get('tipo')
        if tipo == 'Piloto':
            return render_template('dashboard_piloto.html')
        if tipo == 'Escuderia':
            return render_template('dashboard_escuderia.html')
        
    @aplicacao.route('/relatorios', methods=['GET'])
    @auth_middleware(tipo_permitido=["Piloto", "Escuderia", "Admin"])
    def view_relatorios(usuario_logado):
        tipo = usuario_logado.get('tipo')
        if tipo == 'Piloto':
            return render_template('relatorios_piloto.html')
        if tipo == 'Escuderia':
            return render_template('relatorios_escuderia.html')
        
    @aplicacao.route('/', methods=['GET'])
    def view_login():
        return render_template('login.html')