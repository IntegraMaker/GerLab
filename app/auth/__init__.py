"""Blueprint auth: entrar e sair do sistema (SPEC-02, UC03 e UC20)."""
from flask import Blueprint

bp = Blueprint("auth", __name__)

from app.auth import routes  # noqa: E402,F401
