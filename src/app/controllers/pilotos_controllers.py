from src.app.BD.pilotos_dao import Pilotos_dao
from src.config.database import connection_pool
from flask import jsonify


class PilotosControllers:
    def __init__(self):
        pass  
    def api_obter_anos_atividade_piloto(self, driver_ref):
        piloto_dao = Pilotos_dao(connection_pool)
        dados, erro = piloto_dao.obter_anos_atividade_piloto(driver_ref)

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code

        # Se tudo tiver ok, retornamos os dados e um status 200 (OK)
        return jsonify(dados), 200
    def api_obter_estatisticas_piloto(self, driver_ref):
        piloto_dao = Pilotos_dao(connection_pool)
        dados, erro = piloto_dao.obter_estatisticas_piloto(driver_ref)

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code

        # Se tudo tiver ok, retornamos os dados e um status 200 (OK)
        return jsonify(dados), 200

    def api_obter_relatorio_6_piloto(self, driver_ref):
        piloto_dao = Pilotos_dao(connection_pool)
        dados, erro = piloto_dao.obter_relatorio_6_piloto(driver_ref)

        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code

        # Se tudo tiver ok, retornamos os dados e um status 200 (OK)
        return jsonify(dados), 200