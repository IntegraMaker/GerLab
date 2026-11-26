"""Modelo Notificacao — os avisos dentro do sistema (SPEC-08 RF-020, Issue #8).

Cada linha é um aviso para UMA pessoa. Ele aponta para o item que o gerou
(ex.: entidade="Equipamento", entidade_id=12) para que, ao abrir o aviso,
o sistema leve até lá — ou mostre "item excluído", se ele não existir mais.
"""
from datetime import datetime, timezone

from app.extensions import db


def _agora_utc():
    return datetime.now(timezone.utc)


class Notificacao(db.Model):
    __tablename__ = "notificacao"

    id = db.Column(db.Integer, primary_key=True)
    destinatario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    texto = db.Column(db.String(300), nullable=False)
    # Para onde o aviso leva (vazio = aviso sem item, só texto).
    entidade = db.Column(db.String(50), nullable=True)
    entidade_id = db.Column(db.Integer, nullable=True)
    criada_em = db.Column(db.DateTime(timezone=True), nullable=False, default=_agora_utc)
    lida_em = db.Column(db.DateTime(timezone=True), nullable=True)   # vazio = não lida

    destinatario = db.relationship("Usuario")

    # O contador pergunta sempre: "quantos avisos NÃO lidos esta pessoa tem?"
    __table_args__ = (db.Index("ix_notificacao_destinatario_lida", "destinatario_id", "lida_em"),)

    @property
    def lida(self):
        return self.lida_em is not None

    def __repr__(self):
        estado = "lida" if self.lida else "não lida"
        return f"<Notificacao {self.id} para={self.destinatario_id} {estado}>"
