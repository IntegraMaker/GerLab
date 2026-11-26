"""Modelo Usuario (SPEC-02 §5)."""
import enum
from datetime import datetime, timezone

from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class Perfil(enum.Enum):
    ESTUDANTE = "ESTUDANTE"
    SERVIDOR = "SERVIDOR"
    ADMINISTRADOR = "ADMINISTRADOR"


def _agora_utc():
    return datetime.now(timezone.utc)


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    # Guardado sempre em minúsculas; único no sistema.
    email = db.Column(db.String(254), nullable=False, unique=True)
    # Nunca a senha em texto: apenas o hash gerado pelo werkzeug.security.
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.Enum(Perfil, name="perfil_usuario"), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    confirmado = db.Column(db.Boolean, nullable=False, default=False)
    data_cadastro = db.Column(db.DateTime(timezone=True), nullable=False, default=_agora_utc)

    @validates("email")
    def _normalizar_email(self, _chave, email):
        # Decisão aprovada: e-mail sempre guardado em minúsculas.
        return email.strip().lower() if email else email

    def definir_senha(self, senha):
        """Guarda só o hash (com sal) da senha, nunca o texto."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.id} {self.email} {self.perfil.name if self.perfil else None}>"
