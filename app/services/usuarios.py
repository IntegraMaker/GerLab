"""Casos de uso de usuários."""
from flask import current_app

from app.domain.senha import problemas_da_senha
from app.extensions import db
from app.models import Perfil, Usuario

# Domínio dos Servidores (SPEC-02 RF-001/RF-002). Só Servidor pode ser Administrador.
DOMINIO_SERVIDOR = "ifpb.edu.br"


class ErroCriacaoUsuario(ValueError):
    """Dados inválidos para criar um usuário; a mensagem é mostrada ao operador."""


def criar_administrador(nome, email, senha):
    """Cria o primeiro Administrador (SPEC-02 §4), já ativo e confirmado."""
    nome = (nome or "").strip()
    email = (email or "").strip().lower()

    if not nome:
        raise ErroCriacaoUsuario("Informe o nome completo.")

    prefixo, arroba, dominio = email.partition("@")
    if not arroba or not prefixo or dominio != DOMINIO_SERVIDOR:
        raise ErroCriacaoUsuario(f"O e-mail do Administrador deve terminar em @{DOMINIO_SERVIDOR}.")

    problemas = problemas_da_senha(senha, prefixo, current_app.config["SENHA_MIN_CARACTERES"])
    if problemas:
        raise ErroCriacaoUsuario(" ".join(problemas))

    if db.session.query(Usuario.id).filter_by(email=email).first():
        raise ErroCriacaoUsuario("Já existe um usuário com esse e-mail.")

    usuario = Usuario(
        nome=nome,
        email=email,
        perfil=Perfil.ADMINISTRADOR,
        ativo=True,
        confirmado=True,
    )
    usuario.definir_senha(senha)
    db.session.add(usuario)
    db.session.commit()
    return usuario
