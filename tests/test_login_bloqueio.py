"""Testes da Issue #5 (P-005), Etapa 3: bloqueio ligado ao login (UC03 FE4)."""
from datetime import datetime, timedelta, timezone

import pytest

from app.extensions import db
from app.models import TentativaLogin
from app.services.autenticacao import ResultadoLogin, autenticar
from tests.test_login import MSG_INVALIDAS, SENHA, _criar_usuario, _entrar, _logado

EMAIL = "maria2024@ifpb.edu.br"
MSG_BLOQUEIO = "Muitas tentativas de entrar. Aguarde 15 minutos e tente de novo."
INICIO = datetime(2026, 11, 26, 10, 0, tzinfo=timezone.utc)


def minutos(n):
    return INICIO + timedelta(minutes=n)


@pytest.fixture
def cliente(app, banco):
    return app.test_client()


def _cliente_no_ip(app, ip):
    """Um "navegador" de teste que parece vir do computador com este IP."""
    cliente = app.test_client()
    cliente.environ_base["REMOTE_ADDR"] = ip
    return cliente


def _errar(cliente, vezes, email=EMAIL):
    for _ in range(vezes):
        resposta = _entrar(cliente, email, "SenhaErrada9")
        assert MSG_INVALIDAS in resposta.get_data(as_text=True)


def test_sexta_tentativa_bloqueada_mesmo_com_senha_correta(cliente, banco):
    # Teste obrigatório 1, pela tela de login.
    _criar_usuario(banco)
    _errar(cliente, 5)

    resposta = _entrar(cliente, EMAIL, SENHA)   # agora com a senha CERTA
    html = resposta.get_data(as_text=True)
    assert MSG_BLOQUEIO in html
    assert not _logado(cliente)


def test_mensagem_de_bloqueio_nao_revela_se_o_email_existe(cliente, banco):
    _criar_usuario(banco)
    _errar(cliente, 5, email="ninguem@ifpb.edu.br")   # e-mail inexistente

    # O mesmo IP também ficou bloqueado; a mensagem é a mesma para os dois.
    existe = _entrar(cliente, EMAIL, SENHA).get_data(as_text=True)
    nao_existe = _entrar(cliente, "ninguem@ifpb.edu.br", SENHA).get_data(as_text=True)
    assert MSG_BLOQUEIO in existe
    assert MSG_BLOQUEIO in nao_existe


def test_ip_diferente_e_conta_sem_falhas_continua_entrando(app, banco):
    # Teste obrigatório 3 (outro lado): outro computador não é afetado.
    # As falhas do "atacante" vão direto pelo serviço: dois navegadores de
    # teste no mesmo contexto misturariam o token CSRF (cache em `g`).
    _criar_usuario(banco)
    _criar_usuario(banco, email="joao2024@ifpb.edu.br")
    for _ in range(5):
        autenticar("joao2024@ifpb.edu.br", "SenhaErrada9", ip="10.0.0.66")
    db.session.commit()

    outro_pc = _cliente_no_ip(app, "10.0.0.7")
    _entrar(outro_pc, EMAIL, SENHA)
    assert _logado(outro_pc)


def test_apos_15_minutos_senha_correta_volta_a_entrar(banco):
    # Teste obrigatório 2, pelo serviço, com relógio simulado.
    _criar_usuario(banco)
    for i in range(5):
        autenticar(EMAIL, "SenhaErrada9", ip="10.0.0.5", agora=minutos(i))
    db.session.commit()

    resultado, _ = autenticar(EMAIL, SENHA, ip="10.0.0.5", agora=minutos(18))
    assert resultado is ResultadoLogin.BLOQUEADO
    resultado, usuario = autenticar(EMAIL, SENHA, ip="10.0.0.5", agora=minutos(19))
    assert resultado is ResultadoLogin.OK
    assert usuario.email == EMAIL


def test_tentativas_durante_o_bloqueio_nao_aumentam_o_castigo(banco):
    _criar_usuario(banco)
    for i in range(5):
        autenticar(EMAIL, "SenhaErrada9", ip="10.0.0.5", agora=minutos(i))
    # Continua tentando (errado) durante o castigo: não é anotado.
    for i in range(10, 15):
        resultado, _ = autenticar(EMAIL, "SenhaErrada9", ip="10.0.0.5", agora=minutos(i))
        assert resultado is ResultadoLogin.BLOQUEADO
    db.session.commit()

    assert db.session.execute(db.select(db.func.count(TentativaLogin.id))).scalar() == 5
    resultado, _ = autenticar(EMAIL, SENHA, ip="10.0.0.5", agora=minutos(19))
    assert resultado is ResultadoLogin.OK


def test_conta_desativada_com_senha_certa_nao_conta_como_falha(banco):
    _criar_usuario(banco, ativo=False)
    for i in range(6):
        resultado, _ = autenticar(EMAIL, SENHA, ip="10.0.0.5", agora=minutos(i))
        assert resultado is ResultadoLogin.DESATIVADA   # nunca vira BLOQUEADO
    db.session.commit()

    falhas = db.session.execute(
        db.select(db.func.count(TentativaLogin.id)).filter_by(sucesso=False)
    ).scalar()
    assert falhas == 0


def test_toda_tentativa_pela_tela_fica_anotada_com_o_ip(app, banco):
    _criar_usuario(banco)
    cliente = _cliente_no_ip(app, "10.0.0.8")
    _entrar(cliente, EMAIL, "SenhaErrada9")
    _entrar(cliente, EMAIL, SENHA)

    anotacoes = db.session.execute(
        db.select(TentativaLogin).order_by(TentativaLogin.id)
    ).scalars().all()
    assert [(a.ip, a.sucesso) for a in anotacoes] == [("10.0.0.8", False), ("10.0.0.8", True)]
