"""Modelo Usuario (SPEC-02 §5)."""
import enum
from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class Perfil(enum.Enum):
    ESTUDANTE = "ESTUDANTE"
    SERVIDOR = "SERVIDOR"
    ADMINISTRADOR = "ADMINISTRADOR"


def _agora_utc():
    return datetime.now(timezone.utc)


class Usuario(UserMixin, db.Model):
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
    # "Botão de emergência": ao aumentar este número, todas as sessões
    # abertas deste usuário deixam de valer (SPEC-02 RF-004, RF-027).
    sessao_versao = db.Column(db.Integer, nullable=False, default=1, server_default="1")

    @validates("email")
    def _normalizar_email(self, _chave, email):
        # Decisão aprovada: e-mail sempre guardado em minúsculas.
        return email.strip().lower() if email else email

    def definir_senha(self, senha):
        """Guarda só o hash (com sal) da senha, nunca o texto."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    # --- Integração com o Flask-Login ---

    def get_id(self):
        """O que fica guardado no cookie de sessão: "id:versão"."""
        return f"{self.id}:{self.sessao_versao}"

    @property
    def is_active(self):
        # Conta desativada pelo Administrador não pode iniciar sessão.
        return self.ativo

    def encerrar_sessoes(self):
        """Invalida todas as sessões abertas deste usuário (sem commit)."""
        self.sessao_versao += 1

    def __repr__(self):
        return f"<Usuario {self.id} {self.email} {self.perfil.name if self.perfil else None}>"


@login_manager.user_loader
def carregar_usuario(id_sessao):
    """Chamado a cada requisição para descobrir quem é o dono da sessão.

    Se a versão guardada no cookie não for a atual (sessões encerradas)
    ou se a conta foi desativada, devolve None: a sessão deixa de valer.
    """
    try:
        id_texto, versao_texto = id_sessao.split(":")
        usuario_id, versao = int(id_texto), int(versao_texto)
    except (AttributeError, ValueError):
        return None
    usuario = db.session.get(Usuario, usuario_id)
    if usuario is None or not usuario.ativo or usuario.sessao_versao != versao:
        return None
    return usuario
