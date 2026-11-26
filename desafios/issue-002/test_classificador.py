"""Testes do microdesafio da Issue #2. NÃO ALTERE este arquivo."""
import pytest

from classificador import classificar_perfil


def test_academico_e_estudante():
    assert classificar_perfil("joao@academico.ifpb.edu.br") == "ESTUDANTE"


def test_ifpb_e_servidor():
    assert classificar_perfil("maria@ifpb.edu.br") == "SERVIDOR"


def test_maiusculas_nao_importam():
    assert classificar_perfil("ANA@IFPB.EDU.BR") == "SERVIDOR"


@pytest.mark.parametrize(
    "email",
    ["ana@gmail.com", "ana@ifpb.edu.br.com", "@ifpb.edu.br", "ana", "ana@xifpb.edu.br"],
)
def test_outros_emails_devolvem_none(email):
    assert classificar_perfil(email) is None
