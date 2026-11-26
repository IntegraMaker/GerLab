"""Testes da Issue #4 (P-004), Etapa 1: sessão do Flask-Login e sessao_versao."""
from datetime import timedelta

import pytest
from flask_login import login_required

from app.models import Perfil, Usuario


@pytest.fixture
def app_protegido(app):
    """Acrescenta, só no teste, uma página que exige login."""
    @app.get("/teste-protegida")
    @login_required
    def pagina_protegida():
        return "conteúdo protegido"

    return app


@pytest.fixture
def cliente(app_protegido, banco):
    return app_protegido.test_client()


def _criar_usuario(banco, email="maria2024@ifpb.edu.br"):
    usuario = Usuario(nome="Maria Teste", email=email, perfil=Perfil.SERVIDOR,
                      ativo=True, confirmado=True)
    usuario.definir_senha("Segredo123")
    banco.session.add(usuario)
    banco.session.commit()
    return usuario


def _abrir_sessao(cliente, usuario):
    """Simula um login já feito, gravando no cookie o que o Flask-Login grava."""
    with cliente.session_transaction() as sessao:
        sessao["_user_id"] = usuario.get_id()
        sessao["_fresh"] = True


def _acessar(cliente, url):
    """Faz a requisição num contexto novo, como no servidor de verdade.

    Sem isso, o Flask-Login reaproveitaria o usuário guardado em `g` na
    requisição anterior do mesmo teste e não conferiria a versão de novo.
    """
    with cliente.application.app_context():
        return cliente.get(url)


def test_sessao_guarda_id_e_versao(banco):
    usuario = _criar_usuario(banco)
    assert usuario.sessao_versao == 1
    assert usuario.get_id() == f"{usuario.id}:1"


def test_sessao_valida_abre_pagina_protegida(cliente, banco):
    usuario = _criar_usuario(banco)
    _abrir_sessao(cliente, usuario)

    resposta = _acessar(cliente, "/teste-protegida")
    assert resposta.status_code == 200


# Teste obrigatório 4: incrementar sessao_versao invalida a sessão existente
def test_incrementar_sessao_versao_invalida_sessao_existente(cliente, banco):
    usuario = _criar_usuario(banco)
    _abrir_sessao(cliente, usuario)
    assert _acessar(cliente, "/teste-protegida").status_code == 200

    usuario.encerrar_sessoes()          # "botão de emergência"
    banco.session.commit()

    resposta = _acessar(cliente, "/teste-protegida")
    assert resposta.status_code == 302
    assert "/entrar" in resposta.headers["Location"]


def test_conta_desativada_perde_a_sessao(cliente, banco):
    usuario = _criar_usuario(banco)
    _abrir_sessao(cliente, usuario)

    usuario.ativo = False
    banco.session.commit()

    assert _acessar(cliente, "/teste-protegida").status_code == 302


def test_sem_sessao_redireciona_ao_login(cliente):
    resposta = _acessar(cliente, "/teste-protegida")
    assert resposta.status_code == 302
    assert "/entrar" in resposta.headers["Location"]


def test_cookie_de_sessao_seguro_e_expira_em_2_horas(app):
    assert app.config["PERMANENT_SESSION_LIFETIME"] == timedelta(hours=2)
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
