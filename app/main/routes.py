from flask import jsonify, render_template
from flask_login import login_required
from sqlalchemy import text

from app.extensions import db
from app.main import bp


@bp.get("/")
@login_required
def inicio():
    # Área logada provisória: o dashboard (Issue #17) vai tomar este lugar.
    return render_template("inicio.html")


@bp.get("/saude")
def saude():
    """Confirma que a aplicação responde e que o banco está acessível."""
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        return jsonify(status="erro", banco="indisponivel"), 503
    return jsonify(status="ok", banco="ok")
