"""Fábrica da aplicação GERLab."""
import os

from flask import Flask

from config import config_por_nome
from app.extensions import csrf, db, migrate


def create_app(nome_config=None):
    nome_config = nome_config or os.environ.get("FLASK_CONFIG", "development")
    app = Flask(__name__)
    app.config.from_object(config_por_nome[nome_config])

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY não definida (veja .env.example).")
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("URL do banco não definida (veja .env.example).")

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app import models  # noqa: F401  (registra os modelos no SQLAlchemy)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import registrar_comandos
    registrar_comandos(app)

    return app
