"""Testes da Issue #4 (P-004), Etapa 2: tela de login e mensagens UC03 FE1-FE3."""
import re

import pytest

from app.models import Perfil, Usuario

SENHA = "Segredo123"
MSG_INVALIDAS = "E-mail ou senha inválidos. Confira os dados e tente de novo."


@pytest.fixture
def cliente(app, banco):
    return app.test_client()


def _criar_usuario(banco, email="maria2024@ifpb.edu.br", ativo=True, confirmado=True):
    usuario = Usuario(nome="Maria Teste", email=email, perfil=Perfil.SERVIDOR,
                      ativo=ativo, confirmado=confirmado)
    usuario.definir_senha(SENHA)
    banco.session.add(usuario)
    banco.session.commit()
    return usuario


def _token_csrf(cliente, url="/entrar"):
    html = cliente.get(url).get_data(as_text=True)
    achado = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', html)
    assert achado, "campo csrf_token não encontrado no formulário"
    return achado.group(1)


def _entrar(cliente, email, senha, url="/entrar"):
    dados = {"email": email, "senha": senha, "csrf_token": _token_csrf(cliente, url)}
    return cliente.post(url, data=dados)


def _logado(cliente):
    with cliente.session_transaction() as sessao:
        return "_user_id" in sessao


def test_pagina_de_login_mostra_o_formulario(cliente):
    html = cliente.get("/entrar").get_data(as_text=True)
    assert "Entrar" in html
    assert 'name="email"' in html
    assert 'name="senha"' in html
    assert 'name="csrf_token"' in html


def test_login_correto_abre_sessao_de_2_horas(cliente, banco):
    _criar_usuario(banco)
    resposta = _entrar(cliente, "maria2024@ifpb.edu.br", SENHA)

    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/"
    assert _logado(cliente)
    # session.permanent = True faz o cookie ter data de validade (2 h)
    assert "Expires=" in resposta.headers["Set-Cookie"]


def test_login_aceita_email_com_maiusculas(cliente, banco):
    _criar_usuario(banco)
    resposta = _entrar(cliente, "  MARIA2024@IFPB.EDU.BR ", SENHA)
    assert resposta.status_code == 302
    assert _logado(cliente)


# Teste obrigatório 1: mensagem genérica idêntica para e-mail inexistente e senha errada
def test_email_inexistente_e_senha_errada_tem_a_mesma_resposta(cliente, banco):
    _criar_usuario(banco)

    inexistente = _entrar(cliente, "ninguem@ifpb.edu.br", SENHA)
    senha_errada = _entrar(cliente, "maria2024@ifpb.edu.br", "Errada999")

    for resposta in (inexistente, senha_errada):
        assert resposta.status_code == 200
        assert MSG_INVALIDAS in resposta.get_data(as_text=True)

    # Tirando o e-mail digitado e o token CSRF (que muda a cada segundo),
    # as duas páginas são idênticas: nada denuncia se o e-mail existe.
    def _sem_partes_variaveis(resposta, email):
        html = resposta.get_data(as_text=True).replace(email, "EMAIL")
        return re.sub(r'(csrf[-_]token"[^>]*?(?:content|value)=")[^"]+', r"\1TOKEN", html)

    assert _sem_partes_variaveis(inexistente, "ninguem@ifpb.edu.br") == \
        _sem_partes_variaveis(senha_errada, "maria2024@ifpb.edu.br")
    assert not _logado(cliente)


# Teste obrigatório 2: conta não confirmada com senha correta → orientação de confirmação
def test_conta_nao_confirmada_recebe_orientacao(cliente, banco):
    _criar_usuario(banco, confirmado=False)

    html = _entrar(cliente, "maria2024@ifpb.edu.br", SENHA).get_data(as_text=True)
    assert "ainda não foi confirmada" in html
    assert not _logado(cliente)


def test_conta_nao_confirmada_com_senha_errada_recebe_mensagem_generica(cliente, banco):
    _criar_usuario(banco, confirmado=False)

    html = _entrar(cliente, "maria2024@ifpb.edu.br", "Errada999").get_data(as_text=True)
    assert MSG_INVALIDAS in html
    assert "confirmada" not in html


def test_conta_desativada_orienta_procurar_coordenacao(cliente, banco):
    _criar_usuario(banco, ativo=False)

    html = _entrar(cliente, "maria2024@ifpb.edu.br", SENHA).get_data(as_text=True)
    assert "desativada" in html
    assert "coordenação" in html
    assert not _logado(cliente)


def test_senha_nunca_volta_para_a_pagina(cliente, banco):
    _criar_usuario(banco)
    html = _entrar(cliente, "maria2024@ifpb.edu.br", "Errada999").get_data(as_text=True)
    assert "Errada999" not in html


@pytest.mark.parametrize("proximo", ["https://site-falso.com", "//site-falso.com", "site-falso.com"])
def test_next_para_fora_do_site_e_ignorado(cliente, banco, proximo):
    _criar_usuario(banco)
    resposta = _entrar(cliente, "maria2024@ifpb.edu.br", SENHA, url=f"/entrar?next={proximo}")
    assert resposta.headers["Location"] == "/"


def test_next_interno_e_respeitado(cliente, banco):
    _criar_usuario(banco)
    resposta = _entrar(cliente, "maria2024@ifpb.edu.br", SENHA, url="/entrar?next=/saude")
    assert resposta.headers["Location"] == "/saude"
