"""Testes do microdesafio da Issue #4. NÃO ALTERE este arquivo."""
import pytest

from portaria import conferir_cracha, sair


@pytest.fixture
def versoes():
    return {7: 1, 8: 3}


def test_cracha_com_versao_atual_e_aceito(versoes):
    assert conferir_cracha("7:1", versoes) == 7


def test_cracha_com_versao_antiga_e_rejeitado(versoes):
    assert conferir_cracha("8:2", versoes) is None


def test_usuario_inexistente_e_rejeitado(versoes):
    assert conferir_cracha("99:1", versoes) is None


def test_sair_aumenta_a_versao(versoes):
    sair(7, versoes)
    assert versoes[7] == 2
    assert versoes[8] == 3  # os outros usuários não mudam


def test_depois_de_sair_o_cracha_antigo_para_de_valer(versoes):
    assert conferir_cracha("7:1", versoes) == 7
    sair(7, versoes)
    assert conferir_cracha("7:1", versoes) is None
    assert conferir_cracha("7:2", versoes) == 7
