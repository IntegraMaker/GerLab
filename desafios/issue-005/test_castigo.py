"""Testes do microdesafio da Issue #5. NÃO ALTERE este arquivo."""
from castigo import esta_de_castigo


def test_quatro_falhas_nao_dao_castigo():
    assert esta_de_castigo([0, 1, 2, 3], agora=5) is False


def test_cinco_falhas_seguidas_dao_castigo():
    assert esta_de_castigo([0, 1, 2, 3, 4], agora=5) is True


def test_castigo_acaba_15_minutos_depois_da_quinta_falha():
    assert esta_de_castigo([0, 1, 2, 3, 4], agora=18) is True
    assert esta_de_castigo([0, 1, 2, 3, 4], agora=19) is False


def test_falhas_espalhadas_demais_nao_dao_castigo():
    # Da 1ª (minuto 0) à 5ª (minuto 20) passaram 20 minutos.
    assert esta_de_castigo([0, 5, 10, 15, 20], agora=21) is False


def test_so_as_cinco_mais_recentes_importam():
    # A falha do minuto 0 é velha, mas as 5 últimas (30 a 34) estão juntas.
    assert esta_de_castigo([0, 30, 31, 32, 33, 34], agora=35) is True
