"""Modelo EmailPendente — a "caixa de saída" de e-mails (SPEC-08 RF-021, Issue #7).

O sistema nunca espera um e-mail sair: ele só grava a "carta" aqui. Um
processo separado (`flask enviar-emails`, serviço `mailer`) entrega depois.
"""
import enum
from datetime import datetime, timezone

from app.extensions import db


def _agora_utc():
    return datetime.now(timezone.utc)


class EstadoEmail(enum.Enum):
    PENDENTE = "PENDENTE"   # na caixa, esperando o carteiro
    ENVIADO = "ENVIADO"     # entregue
    FALHA = "FALHA"         # falha final: 3 tentativas sem sucesso, não tenta mais


class EmailPendente(db.Model):
    __tablename__ = "email_pendente"

    id = db.Column(db.Integer, primary_key=True)
    destinatario = db.Column(db.String(254), nullable=False)
    assunto = db.Column(db.String(200), nullable=False)
    corpo = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Enum(EstadoEmail, name="estado_email"), nullable=False,
                       default=EstadoEmail.PENDENTE)
    tentativas = db.Column(db.Integer, nullable=False, default=0)
    ultimo_erro = db.Column(db.Text, nullable=True)       # o que deu errado na última tentativa
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=_agora_utc)
    enviado_em = db.Column(db.DateTime(timezone=True), nullable=True)

    # O carteiro sempre pergunta: "quais cartas estão PENDENTES?"
    __table_args__ = (db.Index("ix_email_pendente_estado", "estado"),)

    def __repr__(self):
        return f"<EmailPendente {self.id} {self.destinatario} {self.estado.name}>"
