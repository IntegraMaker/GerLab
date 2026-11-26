"""Testes das telas de avisos (Issue #8, Etapa 2).

Ainda não existem equipamentos de verdade, então o "item" dos avisos é um
modelo que só existe nos testes (com exclusão lógica, como na Issue #3).
"""
from flask import Blueprint

import pytest

from app.domain.exclusao import ExclusaoLogicaMixin
from app.extensions import db
from app.models import Notificacao, Perfil
from app.services import notificacoes as servico
from tests.test_autorizacao import _cliente_logado


class ItemDeAviso(ExclusaoLogicaMixin, db.Model):
    __tablename__ = "item_teste_aviso"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


@pytest.fixture
def app(app):
    bp = Blueprint("teste_avisos", __name__)

    @bp.get("/teste/item/<int:id>")
    def item(id):
        return f"página do item {id}"

    app.register_blueprint(bp)
    app.config["WTF_CSRF_ENABLED"] = False   # foco: permissões e regras dos avisos
    servico.registrar_destino("ItemDeAviso", ItemDeAviso, "teste_avisos.item")
    return app


@pytest.fixture
def pessoas(app, banco):
    """Ana e Bruno logáveis; cada uma com seus avisos."""
    return {
        "ana": _cliente_logado(app, banco, Perfil.SERVIDOR, "ana@ifpb.edu.br"),
        "bruno": _cliente_logado(app, banco, Perfil.ESTUDANTE, "bruno@academico.ifpb.edu.br"),
    }


def _usuario(email):
    from app.models import Usuario
    return db.session.execute(db.select(Usuario).filter_by(email=email)).scalar_one()


def _avisar(email, texto, item=None):
    aviso = Notificacao(destinatario_id=_usuario(email).id, texto=texto,
                        entidade="ItemDeAviso" if item else None,
                        entidade_id=item.id if item else None)
    db.session.add(aviso)
    db.session.commit()
    return aviso


def test_usuario_nao_acessa_aviso_de_outro(pessoas):
    # Teste obrigatório 2: Bruno tenta abrir um aviso da Ana.
    aviso_da_ana = _avisar("ana@ifpb.edu.br", "Chamado aberto no PC-07")

    resposta = pessoas["bruno"].post(f"/avisos/{aviso_da_ana.id}/abrir")

    assert resposta.status_code == 404
    db.session.refresh(aviso_da_ana)
    assert aviso_da_ana.lida is False                # nada mudou


def test_lista_mostra_so_os_proprios_avisos(pessoas):
    _avisar("ana@ifpb.edu.br", "Aviso da Ana")
    _avisar("bruno@academico.ifpb.edu.br", "Aviso do Bruno")

    html = pessoas["bruno"].get("/avisos").get_data(as_text=True)
    assert "Aviso do Bruno" in html
    assert "Aviso da Ana" not in html


def test_marcar_todas_zera_so_o_contador_do_usuario(pessoas):
    # Teste obrigatório 3
    for i in range(3):
        _avisar("ana@ifpb.edu.br", f"Aviso {i} da Ana")
    for i in range(2):
        _avisar("bruno@academico.ifpb.edu.br", f"Aviso {i} do Bruno")

    resposta = pessoas["ana"].post("/avisos/marcar-todas")

    assert resposta.status_code == 302
    assert servico.contar_nao_lidas(_usuario("ana@ifpb.edu.br")) == 0
    assert servico.contar_nao_lidas(_usuario("bruno@academico.ifpb.edu.br")) == 2


def test_abrir_aviso_marca_como_lido_e_leva_ao_item(pessoas):
    item = ItemDeAviso(nome="PC-07")
    db.session.add(item)
    db.session.commit()
    aviso = _avisar("ana@ifpb.edu.br", "Falha no PC-07", item=item)

    resposta = pessoas["ana"].post(f"/avisos/{aviso.id}/abrir")

    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith(f"/teste/item/{item.id}")
    db.session.refresh(aviso)
    assert aviso.lida is True


def test_item_excluido_aviso_continua_e_mostra_item_excluido(pessoas):
    # Cenário 4 da SPEC-08
    item = ItemDeAviso(nome="PC-07")
    db.session.add(item)
    db.session.commit()
    aviso = _avisar("ana@ifpb.edu.br", "Falha no PC-07", item=item)
    item.excluir(_usuario("ana@ifpb.edu.br"))
    db.session.commit()

    html = pessoas["ana"].get("/avisos").get_data(as_text=True)
    assert "Falha no PC-07" in html                  # o aviso continua na lista
    assert "item excluído" in html

    resposta = pessoas["ana"].post(f"/avisos/{aviso.id}/abrir", follow_redirects=True)
    assert "O item deste aviso foi excluído." in resposta.get_data(as_text=True)
    db.session.refresh(aviso)
    assert aviso.lida is True                        # e é marcado como lido


def test_nao_autenticado_vai_para_o_login(app, banco):
    resposta = app.test_client().get("/avisos")
    assert resposta.status_code == 302
    assert "/entrar" in resposta.headers["Location"]
