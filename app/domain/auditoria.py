"""Registro de auditoria na mesma transação da alteração (SPEC-01 RF-016).

Uso, dentro de um serviço:

    sala.nome = novo_nome
    registrar_evento(autor, "Sala", sala.id, "EDITAR",
                     anterior={"nome": antigo}, novo={"nome": novo_nome})
    db.session.commit()   # grava a alteração E o log juntos — ou nenhum dos dois

A função NÃO faz commit: quem chama faz um único commit no fim. Se o log
falhar, o commit falha e a alteração também é desfeita.
"""
from app.extensions import db
from app.models import LogEvento


def registrar_evento(autor, entidade, entidade_id, acao, anterior=None, novo=None):
    evento = LogEvento(
        autor=autor,
        entidade=entidade,
        entidade_id=entidade_id,
        acao=acao,
        valor_anterior=anterior,
        valor_novo=novo,
    )
    db.session.add(evento)
    return evento
