"""Testes do microdesafio da Issue #3. NÃO ALTERE este arquivo."""
from datetime import datetime

import pytest

from lixeira import excluir, listar

QUANDO = datetime(2026, 11, 26, 10, 0)


@pytest.fixture
def pcs():
    return [
        {"nome": "PC-01", "excluido_em": None, "excluido_por": None},
        {"nome": "PC-07", "excluido_em": None, "excluido_por": None},
        {"nome": "PC-09", "excluido_em": None, "excluido_por": None},
    ]


def nomes(lista):
    return [pc["nome"] for pc in lista]


def test_excluir_marca_quando_e_quem(pcs):
    excluir(pcs[1], "admin@ifpb.edu.br", QUANDO)
    assert pcs[1]["excluido_em"] == QUANDO
    assert pcs[1]["excluido_por"] == "admin@ifpb.edu.br"


def test_excluir_nao_apaga_da_lista_original(pcs):
    excluir(pcs[1], "admin@ifpb.edu.br", QUANDO)
    assert nomes(pcs) == ["PC-01", "PC-07", "PC-09"]


def test_listar_esconde_excluidos_por_padrao(pcs):
    excluir(pcs[1], "admin@ifpb.edu.br", QUANDO)
    assert nomes(listar(pcs)) == ["PC-01", "PC-09"]


def test_listar_inclui_excluidos_quando_pedido(pcs):
    excluir(pcs[1], "admin@ifpb.edu.br", QUANDO)
    assert nomes(listar(pcs, incluir_excluidos=True)) == ["PC-01", "PC-07", "PC-09"]


def test_listar_sem_exclusoes_mostra_todos(pcs):
    assert nomes(listar(pcs)) == ["PC-01", "PC-07", "PC-09"]
