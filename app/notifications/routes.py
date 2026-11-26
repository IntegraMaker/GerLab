"""Rotas dos avisos (UC07). Cada pessoa só vê e mexe nos PRÓPRIOS avisos."""
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user

from app.auth.decoradores import exige
from app.domain.permissoes import Acao, pode
from app.extensions import db
from app.notifications import bp
from app.services import notificacoes as servico

# Código especial do HTMX: "pare de perguntar". Usado quando a sessão acabou,
# para o sino não ficar pedindo a página de login a cada 60 segundos.
PARAR_DE_ATUALIZAR = 286


@bp.app_context_processor
def _sino_no_cabecalho():
    """Deixa `nao_lidas` disponível no base.html (sino do cabeçalho)."""
    if current_user.is_authenticated and pode(current_user, Acao.VER_PROPRIAS_NOTIFICACOES):
        return {"nao_lidas_cabecalho": servico.contar_nao_lidas(current_user)}
    return {}


@bp.get("/avisos/contador")
def contador():
    """Pedacinho com o sino atualizado (pedido pelo HTMX a cada 60 s)."""
    if not current_user.is_authenticated or not pode(current_user, Acao.VER_PROPRIAS_NOTIFICACOES):
        return "", PARAR_DE_ATUALIZAR
    return render_template("_partials/contador_avisos.html",
                           nao_lidas=servico.contar_nao_lidas(current_user))


@bp.get("/avisos")
@exige(Acao.VER_PROPRIAS_NOTIFICACOES)
def lista():
    return render_template(
        "notificacoes/lista.html",
        avisos=servico.avisos_de(current_user),
        item_excluido=servico.item_excluido,
        nao_lidas=servico.contar_nao_lidas(current_user),
    )


@bp.post("/avisos/<int:aviso_id>/abrir")
@exige(Acao.VER_PROPRIAS_NOTIFICACOES)
def abrir(aviso_id):
    # Aviso de outra pessoa → 404, como se não existisse (não revela nada).
    aviso = servico.aviso_do_usuario(current_user, aviso_id)
    if aviso is None:
        abort(404)
    servico.marcar_como_lida(aviso)
    db.session.commit()

    destino = servico.destino_do_aviso(aviso)
    if destino:
        return redirect(destino)
    if aviso.entidade:
        flash("O item deste aviso foi excluído.", "warning")
    return redirect(url_for("notifications.lista"))


@bp.post("/avisos/marcar-todas")
@exige(Acao.VER_PROPRIAS_NOTIFICACOES)
def marcar_todas():
    servico.marcar_todas_como_lidas(current_user)
    db.session.commit()
    flash("Todos os avisos foram marcados como lidos.", "success")
    return redirect(url_for("notifications.lista"))
