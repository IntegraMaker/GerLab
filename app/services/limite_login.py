"""Limite de tentativas de login (SPEC-02 RNF-004, Issue #5).

Regra: 5 falhas em 15 minutos, para o mesmo e-mail **ou** o mesmo IP,
bloqueiam novas tentativas por 15 minutos, contados a partir da 5ª falha.
Os números vêm do config (LOGIN_MAX_FALHAS, LOGIN_JANELA_MINUTOS,
LOGIN_BLOQUEIO_MINUTOS).

"Relógio simulado": as funções recebem `agora`. Na vida real ninguém passa
nada e usamos a hora atual; nos testes passamos uma hora inventada, assim
dá para "pular 15 minutos" sem esperar de verdade.
"""
from datetime import datetime, timedelta, timezone

from flask import current_app

from app.extensions import db
from app.models import TentativaLogin


def _agora_ou(agora):
    return agora or datetime.now(timezone.utc)


def _normalizar(email):
    return (email or "").strip().lower()


def registrar_tentativa(email, ip, sucesso, agora=None):
    """Anota uma tentativa no caderno (sem commit: quem chama decide)."""
    tentativa = TentativaLogin(
        email=_normalizar(email), ip=ip or "", sucesso=sucesso, data_hora=_agora_ou(agora)
    )
    db.session.add(tentativa)
    return tentativa


def _bloqueado_por(filtro, agora):
    """Confere um critério (e-mail ou IP) e diz se ele está bloqueado."""
    maximo = current_app.config["LOGIN_MAX_FALHAS"]
    janela = timedelta(minutes=current_app.config["LOGIN_JANELA_MINUTOS"])
    bloqueio = timedelta(minutes=current_app.config["LOGIN_BLOQUEIO_MINUTOS"])

    # As últimas `maximo` falhas, da mais nova para a mais antiga.
    # Só olhamos um período recente: falhas mais velhas não podem bloquear.
    falhas = db.session.execute(
        db.select(TentativaLogin.data_hora)
        .where(filtro, TentativaLogin.sucesso.is_(False))
        .where(TentativaLogin.data_hora <= agora)
        .where(TentativaLogin.data_hora > agora - janela - bloqueio)
        .order_by(TentativaLogin.data_hora.desc())
        .limit(maximo)
    ).scalars().all()

    if len(falhas) < maximo:
        return False
    mais_nova, mais_antiga = falhas[0], falhas[-1]
    aconteceram_na_janela = mais_nova - mais_antiga <= janela
    ainda_de_castigo = agora < mais_nova + bloqueio
    return aconteceram_na_janela and ainda_de_castigo


def esta_bloqueado(email, ip, agora=None):
    """True se o e-mail **ou** o IP estiver bloqueado neste momento."""
    agora = _agora_ou(agora)
    return (
        _bloqueado_por(TentativaLogin.email == _normalizar(email), agora)
        or _bloqueado_por(TentativaLogin.ip == (ip or ""), agora)
    )
