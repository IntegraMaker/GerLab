"""Testes do sino com contador no cabeçalho (Issue #8, Etapa 3)."""
import pytest

from app.extensions import db
from app.models import Notificacao, Perfil, Usuario
from tests.test_autorizacao import _cliente_logado

EMAIL = "ana@ifpb.edu.br"


@pytest.fixture
def ana(app, banco):
    return _cliente_logado(app, banco, Perfil.SERVIDOR, EMAIL)


def _avisos(quantos, email=EMAIL):
    usuario = db.session.execute(db.select(Usuario).filter_by(email=email)).scalar_one()
    for i in range(quantos):
        db.session.add(Notificacao(destinatario_id=usuario.id, texto=f"Aviso {i}"))
    db.session.commit()


def test_cabecalho_mostra_o_sino_com_as_nao_lidas(ana):
    _avisos(3)
    html = ana.get("/").get_data(as_text=True)
    assert 'id="contador-avisos"' in html
    assert 'aria-label="Notificações, 3 não lidas"' in html   # texto do protótipo
    assert 'hx-get="/avisos/contador"' in html


def test_contador_htmx_devolve_so_o_sino(ana):
    _avisos(1)
    resposta = ana.get("/avisos/contador", headers={"HX-Request": "true"})
    html = resposta.get_data(as_text=True)
    assert resposta.status_code == 200
    assert "<html" not in html                                  # só o pedacinho
    assert 'aria-label="Notificações, 1 não lida"' in html       # singular


def test_sem_avisos_nao_mostra_numero(ana):
    html = ana.get("/avisos/contador").get_data(as_text=True)
    assert 'aria-label="Notificações, nenhuma não lida"' in html
    assert "badge" not in html


def test_mais_de_99_mostra_99_mais(ana):
    _avisos(120)
    html = ana.get("/avisos/contador").get_data(as_text=True)
    assert "99+" in html
    assert 'aria-label="Notificações, 120 não lidas"' in html


def test_sessao_encerrada_para_de_atualizar(app, banco):
    resposta = app.test_client().get("/avisos/contador", headers={"HX-Request": "true"})
    assert resposta.status_code == 286        # HTMX para de perguntar
    assert resposta.get_data(as_text=True) == ""


def test_pagina_de_login_nao_tem_sino(app, banco):
    html = app.test_client().get("/entrar").get_data(as_text=True)
    assert "contador-avisos" not in html
