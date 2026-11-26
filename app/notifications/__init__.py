"""Blueprint notifications: avisos dentro do sistema (SPEC-08 RF-020, UC07)."""
from flask import Blueprint

bp = Blueprint("notifications", __name__)

from app.notifications import routes  # noqa: E402,F401
