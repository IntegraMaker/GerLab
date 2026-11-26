"""Testes do modelo TentativaLogin (Issue #5, Etapa 1)."""
from datetime import datetime, timezone

from app.extensions import db
from app.models import TentativaLogin


def test_anota_tentativa_com_data_automatica(banco):
    tentativa = TentativaLogin(email="ana@ifpb.edu.br", ip="10.0.0.5", sucesso=False)
    db.session.add(tentativa)
    db.session.commit()

    salva = db.session.get(TentativaLogin, tentativa.id)
    assert salva.email == "ana@ifpb.edu.br"
    assert salva.ip == "10.0.0.5"
    assert salva.sucesso is False
    assert salva.data_hora is not None


def test_aceita_email_que_nao_existe_e_ipv6(banco):
    # Não há nenhum Usuario no banco: a tentativa é anotada mesmo assim.
    ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    db.session.add(TentativaLogin(email="ninguem@ifpb.edu.br", ip=ipv6, sucesso=False))
    db.session.commit()

    assert db.session.execute(
        db.select(TentativaLogin).filter_by(email="ninguem@ifpb.edu.br")
    ).scalar_one().ip == ipv6


def test_data_hora_pode_ser_informada(banco):
    # Na Etapa 2 os testes usam um "relógio simulado": a data é passada à mão.
    quando = datetime(2026, 11, 26, 10, 0, tzinfo=timezone.utc)
    db.session.add(TentativaLogin(email="a@ifpb.edu.br", ip="1.1.1.1", sucesso=True, data_hora=quando))
    db.session.commit()

    assert db.session.execute(db.select(TentativaLogin)).scalar_one().data_hora == quando
