"""Testes do decorador @exige e da página 403 (Issue #6, Etapa 2).

A aplicação ainda não tem telas de Administrador, então criamos rotas
**só de teste** (um blueprint que existe apenas aqui).
"""
from flask import Blueprint

import pytest

from app.auth.decoradores import exige
from app.domain.permissoes import Acao
from app.models import Perfil, Usuario

# Lista que a rota POST altera: serve para provar que, com 403, nada mudou.
ALTERACOES = []


def _blueprint_de_teste():
    bp = Blueprint("teste_perm", __name__)

    @bp.get("/teste/usuarios")
    @exige(Acao.GERENCIAR_USUARIOS)
    def area_do_admin():
        return "área do Administrador"

    @bp.post("/teste/chamados")
    @exige(Acao.SOLICITAR_CHAMADO)
    def solicitar_chamado():
        ALTERACOES.append("chamado")
        return "chamado solicitado"

    return bp


@pytest.fixture
def app(app):
    # Mesmo nome da fixture do conftest: pega a app de lá e acrescenta as rotas.
    app.register_blueprint(_blueprint_de_teste())
    app.config["WTF_CSRF_ENABLED"] = False   # aqui o foco é a permissão, não o CSRF
    ALTERACOES.clear()
    return app


def _cliente_logado(app, banco, perfil, email):
    usuario = Usuario(nome=f"Pessoa {perfil.name}", email=email, perfil=perfil,
                      ativo=True, confirmado=True)
    usuario.definir_senha("Segredo123")
    banco.session.add(usuario)
    banco.session.commit()

    cliente = app.test_client()
    with cliente.session_transaction() as sessao:   # "entrega o crachá" direto
        sessao["_user_id"] = usuario.get_id()
        sessao["_fresh"] = True
    return cliente


def test_estudante_em_rota_de_administrador_recebe_403(app, banco):
    # Teste obrigatório 1
    cliente = _cliente_logado(app, banco, Perfil.ESTUDANTE, "aluno@academico.ifpb.edu.br")
    resposta = cliente.get("/teste/usuarios")
    assert resposta.status_code == 403
    assert "Acesso negado" in resposta.get_data(as_text=True)


def test_administrador_em_rota_de_administrador_recebe_200(app, banco):
    # Teste obrigatório 2
    cliente = _cliente_logado(app, banco, Perfil.ADMINISTRADOR, "admin@ifpb.edu.br")
    resposta = cliente.get("/teste/usuarios")
    assert resposta.status_code == 200
    assert "área do Administrador" in resposta.get_data(as_text=True)


def test_nao_autenticado_vai_para_o_login(app, banco):
    # Teste obrigatório 3
    resposta = app.test_client().get("/teste/usuarios")
    assert resposta.status_code == 302
    assert "/entrar" in resposta.headers["Location"]
    assert "next=" in resposta.headers["Location"]   # volta para cá depois de entrar


def test_403_nao_executa_a_rota_nem_altera_nada(app, banco):
    # Estudante tenta um POST de Servidor: a rota nem roda.
    cliente = _cliente_logado(app, banco, Perfil.ESTUDANTE, "aluno@academico.ifpb.edu.br")
    resposta = cliente.post("/teste/chamados")
    assert resposta.status_code == 403
    assert ALTERACOES == []


def test_administrador_nao_solicita_chamado(app, banco):
    # A matriz não é uma escada: até o Administrador recebe 403 aqui.
    cliente = _cliente_logado(app, banco, Perfil.ADMINISTRADOR, "admin@ifpb.edu.br")
    assert cliente.post("/teste/chamados").status_code == 403


def test_servidor_solicita_chamado(app, banco):
    cliente = _cliente_logado(app, banco, Perfil.SERVIDOR, "servidor@ifpb.edu.br")
    assert cliente.post("/teste/chamados").status_code == 200
    assert ALTERACOES == ["chamado"]


def test_template_esconde_botao_de_quem_nao_pode(app, banco):
    # Helper `pode` disponível nos templates (a conferência real é no servidor).
    modelo = app.jinja_env.from_string(
        "{% if pode(usuario, Acao.GERENCIAR_USUARIOS) %}BOTAO{% endif %}"
    )
    estudante = Usuario(nome="A", email="a@academico.ifpb.edu.br", perfil=Perfil.ESTUDANTE, ativo=True)
    admin = Usuario(nome="B", email="b@ifpb.edu.br", perfil=Perfil.ADMINISTRADOR, ativo=True)
    assert modelo.render(usuario=estudante) == ""
    assert modelo.render(usuario=admin) == "BOTAO"
