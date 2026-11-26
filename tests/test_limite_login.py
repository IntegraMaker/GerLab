"""Testes da regra de bloqueio (Issue #5, Etapa 2) com relógio simulado."""
from datetime import datetime, timedelta, timezone

from app.extensions import db
from app.services.limite_login import esta_bloqueado, registrar_tentativa

INICIO = datetime(2026, 11, 26, 10, 0, tzinfo=timezone.utc)
IP = "10.0.0.5"


def minutos(n):
    return INICIO + timedelta(minutes=n)


def falhar(vezes, email="ana@ifpb.edu.br", ip=IP, a_partir_de=0):
    """Anota `vezes` falhas, uma por minuto, começando em `a_partir_de`."""
    for i in range(vezes):
        registrar_tentativa(email, ip, sucesso=False, agora=minutos(a_partir_de + i))
    db.session.commit()


def test_4_falhas_ainda_nao_bloqueiam(banco):
    falhar(4)
    assert esta_bloqueado("ana@ifpb.edu.br", IP, agora=minutos(5)) is False


def test_5_falhas_bloqueiam_a_proxima_tentativa(banco):
    # Teste obrigatório 1 (parte da regra): depois de 5 falhas, a 6ª é barrada.
    falhar(5)  # minutos 0, 1, 2, 3, 4
    assert esta_bloqueado("ana@ifpb.edu.br", IP, agora=minutos(5)) is True


def test_apos_15_minutos_volta_a_permitir(banco):
    # Teste obrigatório 2: o castigo dura 15 min a partir da 5ª falha (minuto 4).
    falhar(5)
    assert esta_bloqueado("ana@ifpb.edu.br", IP, agora=minutos(18)) is True
    assert esta_bloqueado("ana@ifpb.edu.br", IP, agora=minutos(19)) is False


def test_contas_diferentes_do_mesmo_ip_bloqueiam(banco):
    # Teste obrigatório 3: cada falha é num e-mail diferente, mas o IP é o mesmo.
    for i in range(5):
        registrar_tentativa(f"pessoa{i}@ifpb.edu.br", IP, sucesso=False, agora=minutos(i))
    db.session.commit()

    assert esta_bloqueado("outra@ifpb.edu.br", IP, agora=minutos(5)) is True
    # Outro computador (outro IP), com um e-mail sem falhas, continua livre.
    assert esta_bloqueado("outra@ifpb.edu.br", "10.0.0.99", agora=minutos(5)) is False


def test_mesmo_email_de_ips_diferentes_bloqueia(banco):
    for i in range(5):
        registrar_tentativa("ana@ifpb.edu.br", f"10.0.0.{i}", sucesso=False, agora=minutos(i))
    db.session.commit()

    assert esta_bloqueado("ANA@ifpb.edu.br ", "10.0.0.99", agora=minutos(5)) is True


def test_falhas_espalhadas_por_mais_de_15_minutos_nao_bloqueiam(banco):
    # Uma falha a cada 5 minutos: entre a 1ª e a 5ª passam 20 minutos.
    for i in range(5):
        registrar_tentativa("ana@ifpb.edu.br", IP, sucesso=False, agora=minutos(i * 5))
    db.session.commit()

    assert esta_bloqueado("ana@ifpb.edu.br", IP, agora=minutos(21)) is False


def test_logins_certos_nao_contam_como_falha(banco):
    for i in range(5):
        registrar_tentativa("ana@ifpb.edu.br", IP, sucesso=True, agora=minutos(i))
    db.session.commit()

    assert esta_bloqueado("ana@ifpb.edu.br", IP, agora=minutos(5)) is False
