from urllib.parse import urlsplit

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import bp
from app.extensions import db
from app.auth.forms import FormularioEntrar
from app.services.autenticacao import ResultadoLogin, autenticar

MENSAGENS = {
    # FE1: a mesma frase para e-mail inexistente e para senha errada.
    ResultadoLogin.CREDENCIAIS_INVALIDAS:
        "E-mail ou senha inválidos. Confira os dados e tente de novo.",
    # FE2: o botão "reenviar confirmação" chega na Issue #10.
    ResultadoLogin.NAO_CONFIRMADA:
        "Sua conta ainda não foi confirmada. Abra o link de confirmação "
        "que enviamos para o seu e-mail institucional.",
    # FE3
    ResultadoLogin.DESATIVADA:
        "Sua conta está desativada. Procure a coordenação do curso.",
}


def _destino_seguro(proximo):
    """Só aceita voltar para uma página do próprio GERLab.

    Impede o golpe do "redirecionamento aberto": um link como
    /entrar?next=https://site-falso.com levaria a pessoa, logo depois
    de entrar, para fora do sistema.
    """
    if not proximo or not proximo.startswith("/") or proximo.startswith("//"):
        return None
    partes = urlsplit(proximo)
    if partes.scheme or partes.netloc:
        return None
    return proximo


@bp.route("/entrar", methods=["GET", "POST"])
def entrar():
    if current_user.is_authenticated:
        return redirect(url_for("main.inicio"))

    formulario = FormularioEntrar()
    erro = None

    if formulario.validate_on_submit():
        resultado, usuario = autenticar(formulario.email.data, formulario.senha.data)
        if resultado is ResultadoLogin.OK:
            login_user(usuario)
            session.permanent = True   # passa a valer o prazo de 2 h sem atividade
            destino = _destino_seguro(request.args.get("next"))
            return redirect(destino or url_for("main.inicio"))
        erro = MENSAGENS[resultado]

    formulario.senha.data = None   # a senha nunca volta para a página
    return render_template("auth/entrar.html", formulario=formulario, erro=erro)


@bp.post("/sair")
@login_required
def sair():
    """Encerra a sessão (SPEC-02 RF-026, UC20 FA2).

    Decisão aprovada pelo estudante (Issue #4): sair aperta o "botão de
    emergência" (sessao_versao + 1). Assim a sessão é invalidada no
    servidor: mesmo uma cópia do cookie deixa de valer. Efeito colateral
    aceito: a pessoa também sai dos outros aparelhos.

    É POST (com token CSRF), e não um link GET, para que outro site não
    consiga deslogar alguém só por incluir uma imagem apontando para /sair.
    """
    current_user.encerrar_sessoes()
    db.session.commit()
    logout_user()
    flash("Você saiu do GERLab.", "success")
    return redirect(url_for("auth.entrar"))
