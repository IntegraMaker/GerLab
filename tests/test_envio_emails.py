"""Testes da "volta do carteiro" (Issue #7, Etapa 2)."""
import smtplib

from app.extensions import db
from app.models import EmailPendente, EstadoEmail
from app.services.emails import enfileirar_email, processar_fila
from app.services.transportes_email import TransporteLog, TransporteSMTP, obter_transporte


class CarteiroDeTeste:
    """Carteiro falso: anota o que "entregou" e pode ser mandado falhar."""

    def __init__(self, falhar=False):
        self.falhar = falhar
        self.entregues = []
        self.tentativas = 0

    def enviar(self, email):
        self.tentativas += 1
        if self.falhar:
            raise smtplib.SMTPServerDisconnected("servidor de e-mail fora do ar")
        self.entregues.append(email.destinatario)


def _um_email(destinatario="ana@ifpb.edu.br"):
    email = enfileirar_email(destinatario, "Confirme seu cadastro", "Clique no link...")
    db.session.commit()
    return email


def test_envio_bem_sucedido_marca_como_enviado(banco):
    # Teste obrigatório 2
    email = _um_email()
    carteiro = CarteiroDeTeste()

    resumo = processar_fila(carteiro)

    assert carteiro.entregues == ["ana@ifpb.edu.br"]
    assert resumo == {"enviados": 1, "falharam": 0, "falha_final": 0}
    db.session.refresh(email)
    assert email.estado is EstadoEmail.ENVIADO
    assert email.enviado_em is not None
    assert email.tentativas == 1


def test_tres_falhas_viram_falha_final_sem_nova_tentativa(banco):
    # Teste obrigatório 3
    email = _um_email()
    carteiro = CarteiroDeTeste(falhar=True)

    processar_fila(carteiro)                 # 1ª tentativa
    db.session.refresh(email)
    assert email.estado is EstadoEmail.PENDENTE and email.tentativas == 1

    processar_fila(carteiro)                 # 2ª
    resumo = processar_fila(carteiro)        # 3ª → desiste
    assert resumo["falha_final"] == 1
    db.session.refresh(email)
    assert email.estado is EstadoEmail.FALHA
    assert email.tentativas == 3
    assert "fora do ar" in email.ultimo_erro

    processar_fila(carteiro)                 # 4ª volta: nem tenta
    assert carteiro.tentativas == 3


def test_falha_de_um_email_nao_atrapalha_os_outros(banco):
    _um_email("ana@ifpb.edu.br")
    _um_email("joao@ifpb.edu.br")

    class FalhaSoParaAna(CarteiroDeTeste):
        def enviar(self, email):
            if email.destinatario.startswith("ana"):
                raise smtplib.SMTPRecipientsRefused({})
            super().enviar(email)

    carteiro = FalhaSoParaAna()
    resumo = processar_fila(carteiro)

    assert carteiro.entregues == ["joao@ifpb.edu.br"]
    assert resumo == {"enviados": 1, "falharam": 1, "falha_final": 0}


def test_emails_ja_enviados_nao_saem_de_novo(banco):
    _um_email()
    carteiro = CarteiroDeTeste()
    processar_fila(carteiro)
    processar_fila(carteiro)
    assert carteiro.entregues == ["ana@ifpb.edu.br"]   # só uma vez


def test_nos_testes_o_carteiro_padrao_so_escreve_no_log(app, banco, caplog):
    assert isinstance(obter_transporte(), TransporteLog)
    email = _um_email()
    with caplog.at_level("INFO"):
        processar_fila()
    assert "ana@ifpb.edu.br" in caplog.text
    db.session.refresh(email)
    assert email.estado is EstadoEmail.ENVIADO


def test_transporte_smtp_monta_e_envia_a_mensagem(app, banco, monkeypatch):
    # SMTP falso: confere o que seria enviado, sem sair para a internet.
    registro = {}

    class SMTPFalso:
        def __init__(self, host, porta, timeout):
            registro["servidor"] = (host, porta, timeout)

        def __enter__(self):
            return self

        def __exit__(self, *erro):
            return False

        def starttls(self):
            registro["tls"] = True

        def login(self, usuario, senha):
            registro["login"] = usuario

        def send_message(self, mensagem):
            registro["mensagem"] = mensagem

    monkeypatch.setattr(smtplib, "SMTP", SMTPFalso)
    carteiro = TransporteSMTP("smtp.gmail.com", 587, "projeto@gmail.com", "senha-de-app",
                              "projeto@gmail.com", timeout=20)
    carteiro.enviar(_um_email())

    assert registro["servidor"] == ("smtp.gmail.com", 587, 20)
    assert registro["tls"] is True
    assert registro["login"] == "projeto@gmail.com"
    assert registro["mensagem"]["To"] == "ana@ifpb.edu.br"
    assert registro["mensagem"]["Subject"] == "Confirme seu cadastro"
