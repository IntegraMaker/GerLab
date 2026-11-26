"""Testes do microdesafio da Issue #1. NÃO ALTERE este arquivo."""
from mini_app import app

cliente = app.test_client()


def test_ola_continua_funcionando():
    resposta = cliente.get("/ola")
    assert resposta.status_code == 200


def test_ping_responde_pong_em_json():
    resposta = cliente.get("/ping")
    assert resposta.status_code == 200
    assert resposta.get_json() == {"resposta": "pong"}


def test_ping_nao_aceita_post():
    # 405 = "método não permitido": a rota existe, mas só aceita GET
    resposta = cliente.post("/ping")
    assert resposta.status_code == 405
