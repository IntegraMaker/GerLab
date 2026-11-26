"""Testes do microdesafio da Issue #7. NÃO ALTERE este arquivo."""
import pytest

from carteiro import dar_uma_volta


def carta(para, estado="PENDENTE", tentativas=0):
    return {"para": para, "estado": estado, "tentativas": tentativas}


def entrega_ok(carta):
    pass   # entregou sem problema


def gmail_fora_do_ar(carta):
    raise ConnectionError("Gmail fora do ar")


def test_entrega_que_da_certo_vira_enviado():
    cartas = [carta("ana@ifpb.edu.br")]
    dar_uma_volta(cartas, entrega_ok)
    assert cartas[0] == {"para": "ana@ifpb.edu.br", "estado": "ENVIADO", "tentativas": 1}


def test_primeira_falha_continua_pendente():
    cartas = [carta("ana@ifpb.edu.br")]
    dar_uma_volta(cartas, gmail_fora_do_ar)
    assert cartas[0]["estado"] == "PENDENTE"
    assert cartas[0]["tentativas"] == 1


def test_terceira_falha_vira_falha_final():
    cartas = [carta("ana@ifpb.edu.br")]
    for _ in range(3):
        dar_uma_volta(cartas, gmail_fora_do_ar)
    assert cartas[0]["estado"] == "FALHA"
    assert cartas[0]["tentativas"] == 3


def test_enviadas_e_falhas_sao_puladas():
    tentou = []

    def anotar(carta):
        tentou.append(carta["para"])

    cartas = [
        carta("ja-foi@ifpb.edu.br", estado="ENVIADO", tentativas=1),
        carta("desistiu@ifpb.edu.br", estado="FALHA", tentativas=3),
        carta("nova@ifpb.edu.br"),
    ]
    dar_uma_volta(cartas, anotar)
    assert tentou == ["nova@ifpb.edu.br"]


def test_falha_de_uma_carta_nao_atrapalha_as_outras():
    def recusa_a_ana(carta):
        if carta["para"].startswith("ana"):
            raise ValueError("endereço recusado")

    cartas = [carta("ana@ifpb.edu.br"), carta("joao@ifpb.edu.br")]
    dar_uma_volta(cartas, recusa_a_ana)
    assert cartas[0]["estado"] == "PENDENTE"
    assert cartas[1]["estado"] == "ENVIADO"
