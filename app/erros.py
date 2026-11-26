"""Páginas de erro do GERLab (Issue #6).

Ficam num lugar só para que toda rota responda do mesmo jeito.

- Página normal → página inteira (erros/403.html, erros/409.html).
- Pedido do HTMX (cabeçalho HX-Request) → só um pedacinho (_partials/erro.html),
  colocado na área de avisos (#avisos) do layout pelos cabeçalhos
  HX-Retarget e HX-Reswap.
"""
from flask import render_template, request

from app.domain.erros import ConflitoDeEstado


def _veio_do_htmx():
    return request.headers.get("HX-Request") == "true"


def _responder(codigo):
    if _veio_do_htmx():
        cabecalhos = {"HX-Retarget": "#avisos", "HX-Reswap": "innerHTML"}
        return render_template("_partials/erro.html", codigo=codigo), codigo, cabecalhos
    return render_template(f"erros/{codigo}.html"), codigo


def registrar_erros(app):
    @app.errorhandler(403)
    def proibido(_erro):
        return _responder(403)

    @app.errorhandler(409)
    def conflito(_erro):
        return _responder(409)

    @app.errorhandler(ConflitoDeEstado)
    def conflito_de_estado(_erro):
        return _responder(409)
