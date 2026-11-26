"""Testes do microdesafio da Issue #6. NÃO ALTERE este arquivo."""
from decisao import decidir


def test_administrador_desfaz_falso_alarme_em_vermelho():
    assert decidir("ADMINISTRADOR", "DESFAZER_FALSO_ALARME", "VERMELHO") == 200


def test_servidor_nao_pode_desfazer_falso_alarme():
    assert decidir("SERVIDOR", "DESFAZER_FALSO_ALARME", "VERMELHO") == 403


def test_estado_ja_mudou_da_409():
    # Outra Administradora já desfez: o PC voltou a Verde.
    assert decidir("ADMINISTRADOR", "DESFAZER_FALSO_ALARME", "VERDE") == 409


def test_permissao_e_conferida_antes_do_estado():
    # Sem permissão E estado errado: a resposta é 403, não 409.
    assert decidir("SERVIDOR", "DESFAZER_FALSO_ALARME", "VERDE") == 403


def test_matriz_nao_e_escada():
    assert decidir("SERVIDOR", "SOLICITAR_CHAMADO", "VERMELHO") == 200
    assert decidir("ADMINISTRADOR", "SOLICITAR_CHAMADO", "VERMELHO") == 403
