"""Testes da fila de e-mails (Issue #7, Etapa 1)."""
import smtplib

import pytest

from app.extensions import db
from app.models import EmailPendente, EstadoEmail
from app.services.emails import enfileirar_email


@pytest.fixture
def smtp_proibido(monkeypatch):
    """Faz qualquer conexão SMTP explodir: se alguém tentar, o teste falha."""
    chamadas = []

    def smtp_falso(*args, **kwargs):
        chamadas.append(args)
        raise AssertionError("enfileirar_email não pode conectar no SMTP")

    monkeypatch.setattr(smtplib, "SMTP", smtp_falso)
    monkeypatch.setattr(smtplib, "SMTP_SSL", smtp_falso)
    return chamadas


def test_enfileirar_nao_chama_o_smtp(banco, smtp_proibido):
    # Teste obrigatório 1
    enfileirar_email("ana@ifpb.edu.br", "Confirme seu cadastro", "Clique no link...")
    db.session.commit()

    assert smtp_proibido == []
    email = db.session.execute(db.select(EmailPendente)).scalar_one()
    assert email.estado is EstadoEmail.PENDENTE
    assert email.tentativas == 0
    assert email.enviado_em is None


def test_enfileirar_guarda_os_dados_da_carta(banco):
    enfileirar_email("  ANA@ifpb.edu.br ", "Assunto", "Corpo do e-mail")
    db.session.commit()

    email = db.session.execute(db.select(EmailPendente)).scalar_one()
    assert email.destinatario == "ana@ifpb.edu.br"
    assert email.assunto == "Assunto"
    assert email.corpo == "Corpo do e-mail"
    assert email.criado_em is not None


def test_enfileirar_vai_junto_com_a_transacao(banco):
    # Sem commit próprio: se a ação que gerou o e-mail for desfeita,
    # o e-mail também some (não sai carta de um cadastro que não aconteceu).
    enfileirar_email("ana@ifpb.edu.br", "Assunto", "Corpo")
    db.session.rollback()

    assert db.session.execute(db.select(db.func.count(EmailPendente.id))).scalar() == 0
