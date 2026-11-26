"""Fábrica da aplicação GERLab."""
import logging
import os

from flask import Flask

from config import config_por_nome
from app.extensions import csrf, db, login_manager, migrate


def create_app(nome_config=None):
    nome_config = nome_config or os.environ.get("FLASK_CONFIG", "development")
    app = Flask(__name__)
    app.config.from_object(config_por_nome[nome_config])
    # Mostra mensagens INFO no log (ex.: o e-mail "enviado" pelo TransporteLog).
    app.logger.setLevel(logging.INFO)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY não definida (veja .env.example).")
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("URL do banco não definida (veja .env.example).")

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app import models  # noqa: F401  (registra os modelos no SQLAlchemy)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.cli import registrar_comandos
    registrar_comandos(app)

    from app.erros import registrar_erros
    registrar_erros(app)

    # Nos templates: {% if pode(current_user, Acao.X) %} mostra o botão só
    # para quem pode usá-lo. A conferência de verdade continua no servidor.
    from app.domain.permissoes import Acao, pode
    app.jinja_env.globals.update(pode=pode, Acao=Acao)

    return app
