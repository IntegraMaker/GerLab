"""Testes do comando `flask enviar-emails` (Issue #7, Etapa 3)."""
from app.extensions import db
from app.models import EmailPendente, EstadoEmail
from app.services.emails import enfileirar_email


def _rodar(app, *args):
    return app.test_cli_runner().invoke(args=["enviar-emails", *args])


def test_uma_volta_entrega_os_pendentes_pelo_log(app, banco):
    enfileirar_email("ana@ifpb.edu.br", "Confirme seu cadastro", "Clique no link...")
    enfileirar_email("joao@ifpb.edu.br", "Recuperação de senha", "Clique no link...")
    db.session.commit()

    resultado = _rodar(app, "--uma-vez")

    assert resultado.exit_code == 0, resultado.output
    assert "transporte: log" in resultado.output
    assert "Enviados: 2" in resultado.output
    estados = db.session.execute(db.select(EmailPendente.estado)).scalars().all()
    assert estados == [EstadoEmail.ENVIADO, EstadoEmail.ENVIADO]


def test_fila_vazia_termina_sem_erro(app, banco):
    resultado = _rodar(app, "--uma-vez")
    assert resultado.exit_code == 0, resultado.output
    assert "Enviados: 0" in resultado.output


def test_falhas_aparecem_no_resumo(app, banco, monkeypatch):
    enfileirar_email("ana@ifpb.edu.br", "Assunto", "Corpo")
    db.session.commit()

    class CarteiroQuebrado:
        def enviar(self, email):
            raise ConnectionError("sem internet")

    monkeypatch.setattr("app.services.emails.obter_transporte", lambda: CarteiroQuebrado())
    resultado = _rodar(app, "--uma-vez")

    assert resultado.exit_code == 0, resultado.output
    assert "falharam: 1" in resultado.output
    email = db.session.execute(db.select(EmailPendente)).scalar_one()
    assert email.estado is EstadoEmail.PENDENTE and email.tentativas == 1
