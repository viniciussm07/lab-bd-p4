from src.app.BD.admin_dao import Admin_dao
from src.config.database import connection_pool
from flask import jsonify


class AdminControllers:
    def __init__(self):
        pass

    def _responder(self, dados, erro):
        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code
        return jsonify(dados), 200

    def api_obter_resumo(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_resumo()
        return self._responder(dados, erro)

    def api_obter_corridas_ultima_temporada(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_corridas_ultima_temporada()
        return self._responder(dados, erro)

    def api_obter_ranking_escuderias(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_ranking_escuderias()
        return self._responder(dados, erro)

    def api_obter_ranking_pilotos(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_ranking_pilotos()
        return self._responder(dados, erro)

    def api_obter_relatorio_contagem_status(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_relatorio_contagem_status()
        return self._responder(dados, erro)

    def api_obter_relatorio_aeroportos(self, cidade):
        if not cidade:
            return jsonify({"erro": "Informe o nome da cidade."}), 400
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_relatorio_aeroportos(cidade)
        return self._responder(dados, erro)

    def api_obter_relatorio_escuderias_pilotos(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_relatorio_escuderias_pilotos()
        return self._responder(dados, erro)

    def api_obter_relatorio_total_corridas(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_relatorio_total_corridas()
        return self._responder(dados, erro)

    def api_obter_relatorio_circuitos(self):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_relatorio_circuitos()
        return self._responder(dados, erro)

    def api_obter_relatorio_corridas_por_circuito(self, circuit_id):
        admin_dao = Admin_dao(connection_pool)
        dados, erro = admin_dao.obter_relatorio_corridas_por_circuito(circuit_id)
        return self._responder(dados, erro)
