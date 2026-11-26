"""Microdesafio da Issue #6: 200, 403 ou 409?

Complete a função `decidir`. Leia o ENUNCIADO.md antes de começar.
"""

# Quem pode fazer cada ação (uma matriz pequena, inspirada na SPEC-01).
MATRIZ = {
    "REPORTAR_FALHA": {"ESTUDANTE", "SERVIDOR", "ADMINISTRADOR"},
    "SOLICITAR_CHAMADO": {"SERVIDOR"},
    "DESFAZER_FALSO_ALARME": {"ADMINISTRADOR"},
}

# Em quais estados do equipamento cada ação vale.
ESTADOS_VALIDOS = {
    "REPORTAR_FALHA": {"VERDE"},                 # só um PC Verde pode virar Vermelho
    "SOLICITAR_CHAMADO": {"VERDE", "VERMELHO"},
    "DESFAZER_FALSO_ALARME": {"VERMELHO"},       # só faz sentido se está Vermelho
}


def decidir(perfil, acao, estado_atual):
    if perfil not in MATRIZ[acao]:
        return 403
    if estado_atual not in ESTADOS_VALIDOS[acao]:
        return 409
    return 200
