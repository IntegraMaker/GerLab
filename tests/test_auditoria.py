"""Testes da Issue #3 (P-003) — auditoria."""
import pytest

from app.domain.auditoria import registrar_evento
from app.models import LogEvento, Perfil, RegistroImutavelError, Usuario


def _usuario(banco, email, perfil=Perfil.SERVIDOR, nome="Usuário Teste"):
    usuario = Usuario(nome=nome, email=email, perfil=perfil)
    usuario.definir_senha("Segredo123")
    banco.session.add(usuario)
    banco.session.commit()
    return usuario


# 1. Registro de log contém autor, entidade, ação, valores anterior e novo
def test_log_contem_autor_entidade_acao_e_valores(banco):
    admin = _usuario(banco, "admin@ifpb.edu.br", Perfil.ADMINISTRADOR)
    servidor = _usuario(banco, "servidor@ifpb.edu.br")

    servidor.perfil = Perfil.ADMINISTRADOR
    registrar_evento(admin, "Usuario", servidor.id, "MUDAR_PERFIL",
                     anterior={"perfil": "SERVIDOR"}, novo={"perfil": "ADMINISTRADOR"})
    banco.session.commit()
    banco.session.expire_all()

    log = LogEvento.query.one()
    assert log.autor.email == "admin@ifpb.edu.br"
    assert log.entidade == "Usuario"
    assert log.entidade_id == servidor.id
    assert log.acao == "MUDAR_PERFIL"
    assert log.valor_anterior == {"perfil": "SERVIDOR"}
    assert log.valor_novo == {"perfil": "ADMINISTRADOR"}
    assert log.data_hora is not None


# 2. Falha no log desfaz a alteração (rollback)
def test_falha_no_log_desfaz_a_alteracao(banco):
    admin = _usuario(banco, "admin@ifpb.edu.br", Perfil.ADMINISTRADOR)
    servidor = _usuario(banco, "servidor@ifpb.edu.br", nome="Nome Antigo")

    servidor.nome = "Nome Novo"
    # Falha forçada: um valor que não pode ser gravado como JSON.
    registrar_evento(admin, "Usuario", servidor.id, "EDITAR",
                     anterior={"nome": "Nome Antigo"}, novo={"nome": object()})
    with pytest.raises(Exception):
        banco.session.commit()
    banco.session.rollback()
    banco.session.expire_all()

    assert banco.session.get(Usuario, servidor.id).nome == "Nome Antigo"
    assert LogEvento.query.count() == 0


# Extra: o registro é imutável (não pode ser alterado nem apagado)
def test_log_nao_pode_ser_alterado(banco):
    admin = _usuario(banco, "admin@ifpb.edu.br", Perfil.ADMINISTRADOR)
    registrar_evento(admin, "Usuario", admin.id, "CRIAR", novo={"perfil": "ADMINISTRADOR"})
    banco.session.commit()

    log = LogEvento.query.one()
    log.acao = "OUTRA_COISA"
    with pytest.raises(RegistroImutavelError):
        banco.session.commit()
    banco.session.rollback()
    assert LogEvento.query.one().acao == "CRIAR"


def test_log_nao_pode_ser_apagado(banco):
    admin = _usuario(banco, "admin@ifpb.edu.br", Perfil.ADMINISTRADOR)
    registrar_evento(admin, "Usuario", admin.id, "CRIAR")
    banco.session.commit()

    banco.session.delete(LogEvento.query.one())
    with pytest.raises(RegistroImutavelError):
        banco.session.commit()
    banco.session.rollback()
    assert LogEvento.query.count() == 1
