from src.app.BD.admin_dao import Admin_dao
from src.config.database import connection_pool
from flask import jsonify, request


class AdminControllers:
    def __init__(self):
        pass

    def _responder(self, dados, erro):
        if erro:
            status_code = 500 if erro == "Erro interno no servidor" else 404
            return jsonify({"erro": erro}), status_code
        return jsonify(dados), 200

    def _responder_cadastro(self, dados, erro):
        if erro:
            status = 500 if erro == "Erro interno no servidor" else 400
            return jsonify({"erro": erro}), status
        return jsonify(dados), 201

    def _obter_json(self):
        return request.get_json(silent=True) or {}

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

    def api_cadastrar_escuderia(self):
        dados = self._obter_json()
        constructor_ref = (dados.get("constructor_ref") or "").strip()
        name = (dados.get("name") or "").strip()
        country_id = dados.get("country_id")
        wikipedia_url = dados.get("wikipedia_url")

        if not constructor_ref or not name or country_id is None:
            return jsonify({
                "erro": "Informe constructor_ref, name e country_id.",
            }), 400

        try:
            country_id = int(country_id)
        except (TypeError, ValueError):
            return jsonify({"erro": "country_id deve ser um número inteiro."}), 400

        if wikipedia_url is not None:
            wikipedia_url = str(wikipedia_url).strip() or None

        admin_dao = Admin_dao(connection_pool)
        resultado, erro = admin_dao.cadastrar_escuderia(
            constructor_ref, name, country_id, wikipedia_url
        )
        return self._responder_cadastro(resultado, erro)

    def api_cadastrar_piloto(self):
        dados = self._obter_json()
        driver_ref = (dados.get("driver_ref") or "").strip()
        given_name = (dados.get("given_name") or "").strip()
        family_name = (dados.get("family_name") or "").strip()
        date_of_birth = (dados.get("date_of_birth") or "").strip()
        country_id = dados.get("country_id")

        if (
            not driver_ref
            or not given_name
            or not family_name
            or not date_of_birth
            or country_id is None
        ):
            return jsonify({
                "erro": "Informe driver_ref, given_name, family_name, date_of_birth e country_id.",
            }), 400

        try:
            country_id = int(country_id)
        except (TypeError, ValueError):
            return jsonify({"erro": "country_id deve ser um número inteiro."}), 400

        admin_dao = Admin_dao(connection_pool)
        resultado, erro = admin_dao.cadastrar_piloto(
            driver_ref, given_name, family_name, date_of_birth, country_id
        )
        return self._responder_cadastro(resultado, erro)
