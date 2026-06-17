from src.app.BD.admin_dao import Admin_dao
from src.config.database import connection_pool
from flask import jsonify


class AdminControllers:
    def __init__(self):
        pass

    def api_obter_resumo(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_resumo()

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code

        return jsonify(dados), 200

    def api_obter_corridas_ultima_temporada(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_corridas_ultima_temporada()

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code

        return jsonify(dados), 200

    def api_obter_ranking_escuderias(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_ranking_escuderias()

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code

        return jsonify(dados), 200

    def api_obter_ranking_pilotos(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_ranking_pilotos()

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code

        return jsonify(dados), 200
