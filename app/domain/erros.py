"""Erros de regra de negócio que viram respostas HTTP (SPEC-01 RN-003).

As regras (services/domain) não conhecem Flask: só levantam estes erros.
O app/erros.py transforma cada um na resposta certa.
"""


class ConflitoDeEstado(Exception):
    """A ação não vale para o estado atual (ex.: outra pessoa já mudou o item).

    Vira HTTP 409, sem alterar nada; a interface recarrega o estado.
    """
