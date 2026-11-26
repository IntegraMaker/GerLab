"""Testes da Issue #4 (P-004), Etapa 3: sair do sistema e página protegida."""
import re

import pytest

from app.extensions import db
from app.models import Perfil, Usuario

SENHA = "Segredo123"


@pytest.fixture
def cliente(app, banco):
    return app.test_client()


def _criar_usuario(banco):
    usuario = Usuario(nome="Maria Teste", email="maria2024@ifpb.edu.br",
                      perfil=Perfil.SERVIDOR, ativo=True, confirmado=True)
    usuario.definir_senha(SENHA)
    banco.session.add(usuario)
    banco.session.commit()
    return usuario.id


def _requisitar(cliente, metodo, url, **kwargs):
    """Cada requisição num contexto novo, como no servidor de verdade
    (veja a explicação em tests/test_sessao.py)."""
    with cliente.application.app_context():
        return getattr(cliente, metodo)(url, **kwargs)


def _token(html):
    return re.search(r'name="csrf_token" (?:type="hidden" )?value="([^"]+)"', html).group(1)


def _entrar(cliente):
    token = _token(_requisitar(cliente, "get", "/entrar").get_data(as_text=True))
    resposta = _requisitar(cliente, "post", "/entrar",
                           data={"email": "maria2024@ifpb.edu.br", "senha": SENHA, "csrf_token": token})
    assert resposta.status_code == 302


def _sair(cliente):
    token = _token(_requisitar(cliente, "get", "/").get_data(as_text=True))
    return _requisitar(cliente, "post", "/sair", data={"csrf_token": token})


def test_pagina_inicial_exige_login(cliente):
    resposta = _requisitar(cliente, "get", "/")
    assert resposta.status_code == 302
    assert "/entrar" in resposta.headers["Location"]


def test_logado_ve_seu_nome_e_o_botao_sair(cliente, banco):
    _criar_usuario(banco)
    _entrar(cliente)

    html = _requisitar(cliente, "get", "/").get_data(as_text=True)
    assert "Olá, Maria Teste" in html
    assert 'action="/sair"' in html


# Teste obrigatório 3: após logout, rota protegida redireciona ao login
def test_apos_sair_pagina_protegida_redireciona_ao_login(cliente, banco):
    _criar_usuario(banco)
    _entrar(cliente)
    assert _requisitar(cliente, "get", "/").status_code == 200

    resposta = _sair(cliente)
    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/entrar"

    depois = _requisitar(cliente, "get", "/")
    assert depois.status_code == 302
    assert "/entrar" in depois.headers["Location"]


def test_sair_invalida_no_servidor_ate_copia_do_cookie(cliente, banco):
    usuario_id = _criar_usuario(banco)
    _entrar(cliente)
    with cliente.session_transaction() as sessao:
        copia_do_cracha = sessao["_user_id"]      # alguém copiou o cookie

    _sair(cliente)

    with cliente.session_transaction() as sessao:  # tenta usar a cópia
        sessao["_user_id"] = copia_do_cracha
        sessao["_fresh"] = True
    assert _requisitar(cliente, "get", "/").status_code == 302
    with cliente.application.app_context():
        assert db.session.get(Usuario, usuario_id).sessao_versao == 2


def test_sair_por_link_get_nao_funciona(cliente, banco):
    _criar_usuario(banco)
    _entrar(cliente)
    assert _requisitar(cliente, "get", "/sair").status_code == 405
    assert _requisitar(cliente, "get", "/").status_code == 200   # continua logado


def test_sair_sem_token_csrf_e_recusado(cliente, banco):
    _criar_usuario(banco)
    _entrar(cliente)
    assert _requisitar(cliente, "post", "/sair").status_code == 400
    assert _requisitar(cliente, "get", "/").status_code == 200


def test_mensagem_de_saida_aparece_no_login(cliente, banco):
    _criar_usuario(banco)
    _entrar(cliente)
    resposta = _sair(cliente)
    html = _requisitar(cliente, "get", resposta.headers["Location"]).get_data(as_text=True)
    assert "Você saiu do GERLab." in html
