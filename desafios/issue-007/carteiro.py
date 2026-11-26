"""Microdesafio da Issue #7: a volta do carteiro.

Complete a função `dar_uma_volta`. Leia o ENUNCIADO.md antes de começar.
"""

MAXIMO_TENTATIVAS = 3

def dar_uma_volta(cartas, entregar):
    for carta in cartas:
        if carta["estado"] != "PENDENTE":
            continue

        carta["tentativas"] += 1

        try:
            entregar(carta)
        except Exception:
            if carta["tentativas"] >= MAXIMO_TENTATIVAS:
                carta["estado"] = "FALHA"
        else:
            carta["estado"] = "ENVIADO"