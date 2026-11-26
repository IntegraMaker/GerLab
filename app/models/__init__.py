"""Entidades SQLAlchemy do GERLab.

Importar os modelos aqui garante que o Flask-Migrate os enxergue.
"""
from app.models.usuario import Perfil, Usuario  # noqa: F401
