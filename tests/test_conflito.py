"""Testes das respostas 409 e dos avisos HTMX (Issue #6, Etapa 3)."""
from flask import Blueprint, abort

import pytest

from app.auth.decoradores import exige
from app.domain.erros import ConflitoDeEstado
from app.domain.permissoes import Acao
from tests.test_autorizacao import _cliente_logado
from app.models import Perfil

HTMX = {"HX-Request": "true"}


def _blueprint_de_teste():
    bp = Blueprint("teste_conflito", __name__)

    @bp.post("/teste/falso-alarme")
    @exige(Acao.MODERAR)
    def desfazer_falso_alarme():
        # Simula a regra de negócio descobrindo que o estado já mudou.
        raise ConflitoDeEstado("o equipamento não está mais Vermelho")

    @bp.post("/teste/abort-409")
    @exige(Acao.VISUALIZAR)
    def abortar():
        abort(409)

    return bp


@pytest.fixture
def app(app):
    app.register_blueprint(_blueprint_de_teste())
    app.config["WTF_CSRF_ENABLED"] = False
    return app


@pytest.fixture
def admin(app, banco):
    return _cliente_logado(app, banco, Perfil.ADMINISTRADOR, "admin@ifpb.edu.br")


def test_409_em_htmx_devolve_fragmento_de_recarga(admin):
    # Teste obrigatório 4
    resposta = admin.post("/teste/falso-alarme", headers=HTMX)
    html = resposta.get_data(as_text=True)

    assert resposta.status_code == 409
    assert "<html" not in html                      # é só um pedaço, não a página
    assert 'data-erro="409"' in html
    assert "Recarregar" in html
    assert resposta.headers["HX-Retarget"] == "#avisos"
    assert resposta.headers["HX-Reswap"] == "innerHTML"


def test_409_sem_htmx_devolve_pagina_inteira(admin):
    resposta = admin.post("/teste/falso-alarme")
    html = resposta.get_data(as_text=True)
    assert resposta.status_code == 409
    assert "<html" in html
    assert "Esta informação mudou" in html
    assert "HX-Retarget" not in resposta.headers


def test_abort_409_tambem_usa_a_mesma_resposta(admin):
    resposta = admin.post("/teste/abort-409", headers=HTMX)
    assert resposta.status_code == 409
    assert 'data-erro="409"' in resposta.get_data(as_text=True)


def test_403_em_htmx_devolve_fragmento(app, banco):
    estudante = _cliente_logado(app, banco, Perfil.ESTUDANTE, "aluno@academico.ifpb.edu.br")
    resposta = estudante.post("/teste/falso-alarme", headers=HTMX)
    html = resposta.get_data(as_text=True)
    assert resposta.status_code == 403
    assert "<html" not in html
    assert 'data-erro="403"' in html
    assert resposta.headers["HX-Retarget"] == "#avisos"


def test_layout_tem_area_de_avisos_e_htmx_configurado(admin):
    html = admin.get("/").get_data(as_text=True)
    assert 'id="avisos"' in html
    assert 'name="htmx-config"' in html
    assert '"40[39]"' in html   # 403 e 409 são mostrados pelo HTMX
