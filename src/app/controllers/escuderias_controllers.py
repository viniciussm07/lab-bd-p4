from src.app.BD.escuderias_dao import Escuderias_dao
from src.config.database import connection_pool
from flask import jsonify


class EscuderiaControllers:
    def __init__(self):
        pass  
    def api_inserir_escuderia_arquivo(self, arquivo):
        if not arquivo:
            return jsonify({"erro": "Nenhum arquivo enviado"}), 400
        escuderia_dao = Escuderias_dao(connection_pool)
        dados, erro = escuderia_dao.inserir_escuderia_arquivo(arquivo)

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code

        # Se tudo tiver ok, retornamos os dados e um status 200 (OK)
        return jsonify(dados), 200
    def api_consultar_piloto_por_sobrenome(self, sobrenome, constructor_ref):
        escuderia_dao = Escuderias_dao(connection_pool)
        dados, erro = escuderia_dao.consultar_piloto_por_sobrenome(sobrenome, constructor_ref)

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code

        # Se tudo tiver ok, retornamos os dados e um status 200 (OK)
        return jsonify(dados), 200
    
    def api_consultar_quantidade_vitorias_escuderia(self, constructor_ref):
        escuderia_dao = Escuderias_dao(connection_pool)
        dados, erro = escuderia_dao.consultar_quantidade_vitorias_escuderia(constructor_ref)

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code
        
        # Se tudo tiver ok, retornamos os dados e um status 200 (OK)
        return jsonify(dados), 200
    def api_consultar_quantidade_pilotos_escuderia(self, constructor_ref):
        escuderia_dao = Escuderias_dao(connection_pool)
        dados, erro = escuderia_dao.consultar_quantidade_pilotos_escuderia(constructor_ref)

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code
        
        # Se tudo tiver ok, retornamos os dados e um status 200 (OK)
        return jsonify(dados), 200
    def api_obter_anos_atividade_escuderia(self, constructor_ref):
        escuderia_dao = Escuderias_dao(connection_pool)
        dados, erro = escuderia_dao.obter_anos_atividade_escuderia(constructor_ref)

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code
        
        # Se tudo tiver ok, retornamos os dados e um status 200 (OK)
        return jsonify(dados), 200
    def api_obter_relatorio_4_escuderia(self, constructor_ref):
        escuderia_dao = Escuderias_dao(connection_pool)
        dados, erro = escuderia_dao.obter_relatorio_4_escuderia(constructor_ref)

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code

        # Se tudo tiver ok, retornamos os dados e um status 200 (OK)
        return jsonify(dados), 200