"""Entidades SQLAlchemy do GERLab.

Importar os modelos aqui garante que o Flask-Migrate os enxergue.
"""
from app.domain.exclusao import ExclusaoLogicaMixin  # noqa: F401  (ativa o filtro padrão)
from app.models.usuario import Perfil, Usuario  # noqa: F401
from app.models.log_evento import LogEvento, RegistroImutavelError  # noqa: F401
from app.models.tentativa_login import TentativaLogin  # noqa: F401
