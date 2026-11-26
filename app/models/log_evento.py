"""Modelo LogEvento — registro imutável de auditoria (SPEC-01 RN-001, RF-016)."""
from datetime import datetime, timezone

from sqlalchemy import event
from sqlalchemy.dialects.postgresql import JSONB

from app.extensions import db


class RegistroImutavelError(RuntimeError):
    """Tentativa de alterar ou apagar um registro de auditoria."""


def _agora_utc():
    return datetime.now(timezone.utc)


class LogEvento(db.Model):
    __tablename__ = "log_evento"

    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime(timezone=True), nullable=False, default=_agora_utc)
    autor_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    # Qual coisa foi alterada: tipo (ex.: "Sala") e o id dela.
    entidade = db.Column(db.String(50), nullable=False)
    entidade_id = db.Column(db.Integer, nullable=False)
    # O que aconteceu (ex.: "CRIAR", "EDITAR", "EXCLUIR", "MUDAR_STATUS").
    acao = db.Column(db.String(50), nullable=False)
    # Valores antes e depois, como dicionários (JSON). Vazios quando não se aplicam.
    valor_anterior = db.Column(JSONB, nullable=True)
    valor_novo = db.Column(JSONB, nullable=True)

    autor = db.relationship("Usuario")

    def __repr__(self):
        return f"<LogEvento {self.id} {self.acao} {self.entidade}#{self.entidade_id}>"


# Imutabilidade: o SQLAlchemy recusa UPDATE e DELETE de qualquer LogEvento.
@event.listens_for(LogEvento, "before_update")
def _impedir_alteracao(_mapper, _conexao, alvo):
    raise RegistroImutavelError(f"Registro de auditoria {alvo.id} não pode ser alterado.")


@event.listens_for(LogEvento, "before_delete")
def _impedir_exclusao(_mapper, _conexao, alvo):
    raise RegistroImutavelError(f"Registro de auditoria {alvo.id} não pode ser apagado.")
