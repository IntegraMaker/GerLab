"""O log da aplicação mostra mensagens INFO (Issue #7): em desenvolvimento,
o e-mail "enviado" pelo TransporteLog precisa aparecer no log do mailer."""
import logging


def test_logger_da_app_aceita_info(app):
    assert app.logger.isEnabledFor(logging.INFO)
