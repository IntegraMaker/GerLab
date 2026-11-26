"""Blueprint principal: página inicial e verificação de saúde."""
from flask import Blueprint

bp = Blueprint("main", __name__)

from app.main import routes  # noqa: E402,F401
