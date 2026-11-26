"""Modelo TentativaLogin — o "caderno da portaria" (SPEC-02 RNF-004, Issue #5).

Cada vez que alguém tenta entrar, anotamos: qual e-mail foi digitado, de
qual IP veio o pedido, quando foi e se deu certo. A regra de bloqueio
(5 falhas em 15 min → 15 min) consulta este caderno.

Guardamos o e-mail **digitado**, e não o id do usuário, porque o e-mail
pode nem existir. Assim um e-mail inexistente também é bloqueado, e o
bloqueio não denuncia quais contas existem.
"""
from datetime import datetime, timezone

from app.extensions import db


def _agora_utc():
    return datetime.now(timezone.utc)


class TentativaLogin(db.Model):
    __tablename__ = "tentativa_login"

    id = db.Column(db.Integer, primary_key=True)
    # E-mail como foi digitado, já em minúsculas e sem espaços nas pontas.
    email = db.Column(db.String(254), nullable=False)
    # 45 caracteres cabem o maior endereço IPv6 escrito por extenso.
    ip = db.Column(db.String(45), nullable=False)
    sucesso = db.Column(db.Boolean, nullable=False)
    data_hora = db.Column(db.DateTime(timezone=True), nullable=False, default=_agora_utc)

    # Índices: as consultas sempre perguntam "falhas deste e-mail (ou deste
    # IP) nos últimos minutos". O índice é como as abas de um fichário.
    __table_args__ = (
        db.Index("ix_tentativa_login_email_data", "email", "data_hora"),
        db.Index("ix_tentativa_login_ip_data", "ip", "data_hora"),
    )

    def __repr__(self):
        estado = "ok" if self.sucesso else "falha"
        return f"<TentativaLogin {self.email} {self.ip} {estado} {self.data_hora}>"
