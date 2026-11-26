"""Avisos dentro do sistema (SPEC-08 RF-020, Issue #8).

As Issues de falhas, chamados e solicitações vão chamar `notificar(...)`
dizendo QUEM deve saber. Este serviço cuida das regras comuns:
- quem executou a ação não recebe aviso dela;
- cada pessoa recebe no máximo um aviso por chamada (sem repetidos);
- sem commit: o aviso é gravado na MESMA transação da ação (RF-021);
- cada pessoa só lê e marca os PRÓPRIOS avisos.
"""
from datetime import datetime, timezone

from flask import url_for

from app.extensions import db
from app.models import Notificacao


def _agora():
    return datetime.now(timezone.utc)


def notificar(destinatarios, autor, texto, entidade=None, entidade_id=None):
    """Cria um aviso para cada destinatário, menos o autor. Devolve os avisos."""
    autor_id = getattr(autor, "id", None)
    ja_avisados = set()
    avisos = []
    for pessoa in destinatarios:
        if pessoa is None or pessoa.id == autor_id or pessoa.id in ja_avisados:
            continue
        ja_avisados.add(pessoa.id)
        aviso = Notificacao(destinatario_id=pessoa.id, texto=texto,
                            entidade=entidade, entidade_id=entidade_id)
        db.session.add(aviso)
        avisos.append(aviso)
    return avisos


# ---------------------------------------------------------------------------
# Para onde cada aviso leva
# ---------------------------------------------------------------------------
# As próximas Issues registram aqui os seus itens, por exemplo:
#     registrar_destino("Equipamento", Equipamento, "labs.equipamento")
# Assim este serviço sabe abrir o item sem conhecer cada modelo.
_DESTINOS = {}


def registrar_destino(entidade, modelo, endpoint):
    _DESTINOS[entidade] = (modelo, endpoint)


def destino_do_aviso(aviso):
    """Endereço do item do aviso; None se o aviso não tem item ou ele foi excluído."""
    if not aviso.entidade or aviso.entidade not in _DESTINOS:
        return None
    modelo, endpoint = _DESTINOS[aviso.entidade]
    item = db.session.get(modelo, aviso.entidade_id)   # o filtro esconde os excluídos
    if item is None or getattr(item, "excluido", False):
        return None
    return url_for(endpoint, id=item.id)


def item_excluido(aviso):
    """True se o aviso apontava para um item que não existe mais."""
    return bool(aviso.entidade) and destino_do_aviso(aviso) is None


# ---------------------------------------------------------------------------
# Leitura e marcação (sempre só os avisos do próprio usuário)
# ---------------------------------------------------------------------------
def avisos_de(usuario, limite=50):
    return db.session.execute(
        db.select(Notificacao)
        .filter_by(destinatario_id=usuario.id)
        .order_by(Notificacao.criada_em.desc(), Notificacao.id.desc())
        .limit(limite)
    ).scalars().all()


def contar_nao_lidas(usuario):
    return db.session.execute(
        db.select(db.func.count(Notificacao.id))
        .filter_by(destinatario_id=usuario.id, lida_em=None)
    ).scalar()


def aviso_do_usuario(usuario, aviso_id):
    """O aviso, se for desta pessoa; senão None (a rota responde 404)."""
    return db.session.execute(
        db.select(Notificacao).filter_by(id=aviso_id, destinatario_id=usuario.id)
    ).scalar_one_or_none()


def marcar_como_lida(aviso):
    if aviso.lida_em is None:
        aviso.lida_em = _agora()


def marcar_todas_como_lidas(usuario):
    """Marca só os avisos desta pessoa (sem commit). Devolve quantos foram marcados."""
    resultado = db.session.execute(
        db.update(Notificacao)
        .where(Notificacao.destinatario_id == usuario.id, Notificacao.lida_em.is_(None))
        .values(lida_em=_agora())
    )
    return resultado.rowcount
