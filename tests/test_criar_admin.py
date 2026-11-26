"""Testes da Issue #2 (P-002) — comando `flask criar-admin`."""
import pytest

from app.models import Perfil, Usuario

SENHA = "Segredo123"


def _rodar(app, email, nome="Ana Admin", senha=SENHA):
    # A senha é digitada duas vezes (pedido + confirmação), como no terminal.
    return app.test_cli_runner().invoke(
        args=["criar-admin", "--nome", nome, "--email", email],
        input=f"{senha}\n{senha}\n",
    )


# 3a. criar-admin cria Administrador ativo e confirmado
def test_criar_admin_cria_administrador_ativo_e_confirmado(app, banco):
    resultado = _rodar(app, "ana.admin@ifpb.edu.br")

    assert resultado.exit_code == 0, resultado.output
    assert "Administrador criado" in resultado.output
    admin = Usuario.query.one()
    assert admin.perfil is Perfil.ADMINISTRADOR
    assert admin.ativo is True
    assert admin.confirmado is True
    assert admin.verificar_senha(SENHA)


# 3b. criar-admin recusa e-mail fora de @ifpb.edu.br
@pytest.mark.parametrize(
    "email",
    ["ana@academico.ifpb.edu.br", "ana@gmail.com", "ana@ifpb.edu.br.com", "ana", "@ifpb.edu.br"],
)
def test_criar_admin_recusa_email_fora_do_dominio(app, banco, email):
    resultado = _rodar(app, email)

    assert resultado.exit_code != 0
    assert "@ifpb.edu.br" in resultado.output
    assert Usuario.query.count() == 0


def test_criar_admin_recusa_senha_fora_da_politica(app, banco):
    resultado = _rodar(app, "ana.admin@ifpb.edu.br", senha="abcdefgh")

    assert resultado.exit_code != 0
    assert "número" in resultado.output
    assert Usuario.query.count() == 0


def test_criar_admin_recusa_email_repetido(app, banco):
    assert _rodar(app, "ana.admin@ifpb.edu.br").exit_code == 0

    resultado = _rodar(app, "ANA.ADMIN@ifpb.edu.br")

    assert resultado.exit_code != 0
    assert "Já existe" in resultado.output
    assert Usuario.query.count() == 1
