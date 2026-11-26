"""Extensões Flask compartilhadas (inicializadas em create_app)."""
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

login_manager = LoginManager()
# Quem não está logado e tenta abrir uma página protegida vai para o login.
login_manager.login_view = "auth.entrar"
login_manager.login_message = "Entre com sua conta para acessar esta página."
login_manager.login_message_category = "warning"
