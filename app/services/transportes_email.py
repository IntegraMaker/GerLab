"""Os "carteiros": jeitos de entregar um e-mail (SPEC-08 RF-021, Issue #7).

- TransporteLog: só escreve a carta no log. Usado em desenvolvimento e testes.
- TransporteSMTP: envia de verdade pelo Gmail do projeto (produção).

Os dois têm o mesmo método `enviar(email)`. Quem processa a fila não
precisa saber qual está usando — só chama `enviar`.
"""
import smtplib
from email.message import EmailMessage

from flask import current_app


class TransporteLog:
    def enviar(self, email):
        current_app.logger.info(
            "E-mail (não enviado, apenas registrado) para=%s assunto=%r\n%s",
            email.destinatario, email.assunto, email.corpo,
        )


class TransporteSMTP:
    def __init__(self, host, porta, usuario, senha, remetente, timeout):
        self.host, self.porta = host, porta
        self.usuario, self.senha = usuario, senha
        self.remetente, self.timeout = remetente, timeout

    def enviar(self, email):
        mensagem = EmailMessage()
        mensagem["From"] = self.remetente
        mensagem["To"] = email.destinatario
        mensagem["Subject"] = email.assunto
        mensagem.set_content(email.corpo)

        with smtplib.SMTP(self.host, self.porta, timeout=self.timeout) as servidor:
            servidor.starttls()                       # conexão protegida
            servidor.login(self.usuario, self.senha)
            servidor.send_message(mensagem)


def obter_transporte():
    """Escolhe o carteiro pelo config (EMAIL_TRANSPORTE = "log" ou "smtp")."""
    config = current_app.config
    if config["EMAIL_TRANSPORTE"] == "smtp":
        return TransporteSMTP(
            host=config["SMTP_HOST"], porta=config["SMTP_PORTA"],
            usuario=config["SMTP_USUARIO"], senha=config["SMTP_SENHA"],
            remetente=config["EMAIL_REMETENTE"] or config["SMTP_USUARIO"],
            timeout=config["SMTP_TIMEOUT_SEGUNDOS"],
        )
    return TransporteLog()
