"""Testes da Issue #2 (P-002) — usuário, hash e política de senha."""
import pytest

from app.domain.senha import problemas_da_senha
from app.models import Perfil, Usuario


def _novo_usuario(email="maria2024@ifpb.edu.br", senha="Segredo123"):
    usuario = Usuario(nome="Maria Teste", email=email, perfil=Perfil.SERVIDOR)
    usuario.definir_senha(senha)
    return usuario


# 1. Senha gravada nunca é igual ao texto
def test_senha_gravada_nunca_e_igual_ao_texto(banco):
    banco.session.add(_novo_usuario(senha="Segredo123"))
    banco.session.commit()
    banco.session.expire_all()

    gravado = Usuario.query.one()
    assert gravado.senha_hash != "Segredo123"
    assert "Segredo123" not in gravado.senha_hash
    assert gravado.verificar_senha("Segredo123") is True
    assert gravado.verificar_senha("Errada123") is False


def test_mesma_senha_gera_hashes_diferentes():
    # O "sal" aleatório faz dois hashes da mesma senha serem diferentes.
    assert _novo_usuario().senha_hash != _novo_usuario().senha_hash


# 2. Política recusa "abcdefgh", "12345678" e senha igual ao prefixo
@pytest.mark.parametrize(
    "senha, prefixo, trecho_esperado",
    [
        ("abcdefgh", "maria", "número"),
        ("12345678", "maria", "letra"),
        ("maria2024", "maria2024", "antes do @"),
        ("MARIA2024", "maria2024", "antes do @"),  # sem diferenciar maiúsculas
        ("abc12", "maria", "8 caracteres"),
    ],
)
def test_politica_recusa_senhas_fracas(senha, prefixo, trecho_esperado):
    problemas = problemas_da_senha(senha, prefixo)
    assert any(trecho_esperado in p for p in problemas), problemas


def test_politica_aceita_senha_valida():
    assert problemas_da_senha("Segredo123", "maria2024") == []


def test_email_e_guardado_em_minusculas(banco):
    banco.session.add(_novo_usuario(email="  Maria2024@IFPB.edu.br "))
    banco.session.commit()
    assert Usuario.query.one().email == "maria2024@ifpb.edu.br"
