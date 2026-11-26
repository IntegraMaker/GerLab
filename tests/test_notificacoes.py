"""Testes do serviço de avisos (Issue #8, Etapa 1)."""
import pytest

from app.extensions import db
from app.models import Notificacao, Perfil, Usuario
from app.services.notificacoes import notificar


def _pessoa(banco, email, perfil=Perfil.ADMINISTRADOR):
    usuario = Usuario(nome=email.split("@")[0], email=email, perfil=perfil,
                      ativo=True, confirmado=True)
    usuario.definir_senha("Segredo123")
    banco.session.add(usuario)
    banco.session.commit()
    return usuario


@pytest.fixture
def administradores(banco):
    return [_pessoa(banco, f"admin{i}@ifpb.edu.br") for i in range(3)]


def _avisos_de(usuario):
    return db.session.execute(
        db.select(Notificacao).filter_by(destinatario_id=usuario.id)
    ).scalars().all()


def test_autor_da_acao_nao_recebe_aviso(banco, administradores):
    # Teste obrigatório 1: o Administrador 0 reporta a falha; avisamos
    # "todos os Administradores", mas ele mesmo fica de fora.
    autor, outro1, outro2 = administradores
    notificar(administradores, autor, "Falha reportada no PC-07",
              entidade="Equipamento", entidade_id=7)
    db.session.commit()

    assert _avisos_de(autor) == []
    assert len(_avisos_de(outro1)) == 1
    assert len(_avisos_de(outro2)) == 1


def test_aviso_guarda_texto_e_item_e_comeca_nao_lido(banco, administradores):
    autor, destinatario, _ = administradores
    notificar([destinatario], autor, "Falha reportada no PC-07",
              entidade="Equipamento", entidade_id=7)
    db.session.commit()

    aviso = _avisos_de(destinatario)[0]
    assert aviso.texto == "Falha reportada no PC-07"
    assert (aviso.entidade, aviso.entidade_id) == ("Equipamento", 7)
    assert aviso.lida is False and aviso.criada_em is not None


def test_mesma_pessoa_duas_vezes_recebe_um_aviso_so(banco, administradores):
    # Ex.: o responsável pelo chamado também é quem reportou a falha.
    autor, destinatario, _ = administradores
    notificar([destinatario, destinatario], autor, "Chamado aberto")
    db.session.commit()
    assert len(_avisos_de(destinatario)) == 1


def test_aviso_vai_junto_com_a_transacao(banco, administradores):
    # Se a ação for desfeita, o aviso também some.
    autor, destinatario, _ = administradores
    notificar([destinatario], autor, "Chamado aberto")
    db.session.rollback()
    assert _avisos_de(destinatario) == []
