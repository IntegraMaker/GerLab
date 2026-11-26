"""O "segurança da porta": decorador @exige (SPEC-01 RN-003, Issue #6).

Uso, em cima de uma rota:

    @bp.post("/salas")
    @exige(Acao.GERENCIAR_CADASTROS)
    def criar_sala(): ...

- Não entrou no sistema → vai para a tela de login (como o @login_required).
- Entrou, mas o perfil não está na matriz → HTTP 403, e a rota nem roda
  (portanto nada é alterado).
"""
from functools import wraps

from flask import abort
from flask_login import current_user

from app.domain.permissoes import pode
from app.extensions import login_manager


def exige(acao):
    def decorador(rota):
        @wraps(rota)
        def rota_protegida(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if not pode(current_user, acao):
                abort(403)
            return rota(*args, **kwargs)
        return rota_protegida
    return decorador
