"""Comandos de terminal do GERLab (`flask <comando>`)."""
import click

from app.services.usuarios import ErroCriacaoUsuario, criar_administrador


@click.command("criar-admin")
@click.option("--nome", prompt="Nome completo", help="Nome completo do Administrador.")
@click.option("--email", prompt="E-mail (@ifpb.edu.br)", help="E-mail institucional do Servidor.")
@click.password_option("--senha", prompt="Senha", confirmation_prompt="Repita a senha",
                       help="Se omitida, é pedida sem aparecer na tela.")
def criar_admin(nome, email, senha):
    """Cria o primeiro Administrador do sistema (ativo e confirmado)."""
    try:
        usuario = criar_administrador(nome, email, senha)
    except ErroCriacaoUsuario as erro:
        raise click.ClickException(str(erro)) from erro
    click.echo(f"Administrador criado: {usuario.email}")


def registrar_comandos(app):
    app.cli.add_command(criar_admin)
