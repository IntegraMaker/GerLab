"""Fila de e-mails (SPEC-08 RF-021, RN-004; Issue #7).

`enfileirar_email` só guarda a carta na caixa de saída: não conecta em
servidor nenhum. Assim a tela responde na hora, mesmo com o Gmail fora do ar.
`processar_fila` é a "volta do carteiro", chamada pelo `flask enviar-emails`.
"""
from datetime import datetime, timezone

from flask import current_app

from app.extensions import db
from app.models import EmailPendente, EstadoEmail
from app.services.transportes_email import obter_transporte


def enfileirar_email(destinatario, assunto, corpo):
    """Coloca um e-mail na fila (sem commit: vai junto com a ação que o gerou)."""
    email = EmailPendente(
        destinatario=(destinatario or "").strip().lower(),
        assunto=assunto,
        corpo=corpo,
        estado=EstadoEmail.PENDENTE,
        tentativas=0,
    )
    db.session.add(email)
    return email


def processar_fila(transporte=None, limite=50):
    """Uma "volta do carteiro": tenta entregar cada e-mail PENDENTE uma vez.

    - Deu certo → ENVIADO (com a hora do envio).
    - Deu errado → conta mais uma tentativa e guarda o erro; na 3ª falha
      vira FALHA (falha final) e nunca mais é tentado.

    Cada e-mail é confirmado (commit) separado: o erro de um não desfaz os
    outros. Devolve quantos foram enviados, quantos falharam nesta volta e
    quantos viraram falha final.
    """
    transporte = transporte or obter_transporte()
    maximo = current_app.config["EMAIL_MAX_TENTATIVAS"]
    resumo = {"enviados": 0, "falharam": 0, "falha_final": 0}

    pendentes = db.session.execute(
        db.select(EmailPendente)
        .where(EmailPendente.estado == EstadoEmail.PENDENTE)
        .order_by(EmailPendente.id)
        .limit(limite)
    ).scalars().all()

    for email in pendentes:
        email.tentativas += 1
        try:
            transporte.enviar(email)
        except Exception as erro:   # qualquer problema de entrega conta como falha
            email.ultimo_erro = f"{type(erro).__name__}: {erro}"[:1000]
            resumo["falharam"] += 1
            if email.tentativas >= maximo:
                email.estado = EstadoEmail.FALHA
                resumo["falha_final"] += 1
                current_app.logger.error(
                    "E-mail %s para %s: falha final após %s tentativas (%s)",
                    email.id, email.destinatario, email.tentativas, email.ultimo_erro,
                )
        else:
            email.estado = EstadoEmail.ENVIADO
            email.enviado_em = datetime.now(timezone.utc)
            email.ultimo_erro = None
            resumo["enviados"] += 1
        db.session.commit()

    return resumo
