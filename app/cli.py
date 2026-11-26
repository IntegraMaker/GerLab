"""Comandos de terminal do GERLab (`flask <comando>`)."""
import time

import click
from flask import current_app

from app.extensions import db
from app.services.emails import processar_fila
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


@click.command("enviar-emails")
@click.option("--uma-vez", is_flag=True, help="Faz uma única volta na fila e termina.")
def enviar_emails(uma_vez):
    """O "carteiro": entrega os e-mails da fila (SPEC-08 RF-021).

    Roda no serviço `mailer` do Docker Compose, separado do site: a cada
    EMAIL_INTERVALO_SEGUNDOS olha a fila e tenta entregar os pendentes.
    """
    intervalo = current_app.config["EMAIL_INTERVALO_SEGUNDOS"]
    transporte = current_app.config["EMAIL_TRANSPORTE"]
    click.echo(f"Carteiro iniciado (transporte: {transporte}, a cada {intervalo} s).")

    while True:
        try:
            resumo = processar_fila()
            if any(resumo.values()) or uma_vez:
                click.echo(
                    f"Enviados: {resumo['enviados']} · falharam: {resumo['falharam']}"
                    f" · falha final: {resumo['falha_final']}"
                )
        except Exception as erro:   # ex.: banco fora do ar — o carteiro não morre
            db.session.rollback()
            current_app.logger.exception("Erro ao processar a fila de e-mails: %s", erro)
            if uma_vez:
                raise
        if uma_vez:
            break
        time.sleep(intervalo)


def registrar_comandos(app):
    app.cli.add_command(criar_admin)
    app.cli.add_command(enviar_emails)
