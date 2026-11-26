"""Testes obrigatórios da Issue #1 (P-001 — ambiente e estrutura inicial)."""
import os
import re


def _registrar_rota_post(app):
    """Rota POST usada apenas nos testes de CSRF (não existe na aplicação)."""
    @app.post("/_teste-post")
    def _teste_post():
        return "ok"


def _extrair_token(html):
    achado = re.search(r'<meta name="csrf-token" content="([^"]+)">', html)
    assert achado, "meta csrf-token não encontrada no layout"
    return achado.group(1)


# 1. create_app("testing") cria a app com configuração de teste
def test_create_app_testing_usa_configuracao_de_teste(app):
    assert app.testing is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.environ["TEST_DATABASE_URL"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] != os.environ.get("DATABASE_URL")
    assert app.config["WTF_CSRF_ENABLED"] is True


# 2. GET /saude retorna 200 e confirma conexão com o banco
def test_saude_retorna_200_com_banco_ok(client):
    resposta = client.get("/saude")
    assert resposta.status_code == 200
    assert resposta.get_json() == {"status": "ok", "banco": "ok"}


# 3. POST sem token CSRF retorna 400
def test_post_sem_token_csrf_retorna_400(app):
    _registrar_rota_post(app)
    resposta = app.test_client().post("/_teste-post", data={"campo": "valor"})
    assert resposta.status_code == 400


# 3b. Complemento: o mesmo POST com o token no cabeçalho X-CSRFToken
# (como faz o static/js/csrf-htmx.js) é aceito.
def test_post_com_token_no_cabecalho_htmx_e_aceito(app):
    _registrar_rota_post(app)
    client = app.test_client()
    token = _extrair_token(client.get("/entrar").get_data(as_text=True))
    resposta = client.post("/_teste-post", headers={"X-CSRFToken": token, "HX-Request": "true"})
    assert resposta.status_code == 200


# 4. Layout base contém <meta name="csrf-token"> e carrega HTMX
def test_layout_base_tem_csrf_token_e_htmx(client):
    # "/" exige login desde a Issue #4; /entrar usa o mesmo layout base
    resposta = client.get("/entrar")
    html = resposta.get_data(as_text=True)
    assert resposta.status_code == 200
    assert _extrair_token(html)
    assert '<script src="/static/vendor/htmx/htmx.min.js"></script>' in html
    assert '<script src="/static/js/csrf-htmx.js"></script>' in html
    assert client.get("/static/vendor/htmx/htmx.min.js").status_code == 200
