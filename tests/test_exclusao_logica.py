"""Testes da Issue #3 (P-003) — exclusão lógica com filtro padrão.

Ainda não existe nenhuma entidade real com exclusão lógica (a Sala vem na
Issue #13), então usamos um modelo que só existe nos testes.
"""
from app.domain.exclusao import INCLUIR_EXCLUIDOS, ExclusaoLogicaMixin
from app.extensions import db
from app.models import Perfil, Usuario


class ItemTeste(ExclusaoLogicaMixin, db.Model):
    __tablename__ = "item_teste_exclusao"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


def _preparar(banco):
    admin = Usuario(nome="Admin", email="admin@ifpb.edu.br", perfil=Perfil.ADMINISTRADOR)
    admin.definir_senha("Segredo123")
    ativo, excluido = ItemTeste(nome="ativo"), ItemTeste(nome="excluido")
    banco.session.add_all([admin, ativo, excluido])
    banco.session.commit()
    excluido.excluir(admin)
    banco.session.commit()
    banco.session.expire_all()
    return admin


# 3a. Entidade com deleted_at não aparece na consulta padrão...
def test_excluido_nao_aparece_na_consulta_padrao(banco):
    _preparar(banco)

    assert [i.nome for i in ItemTeste.query.all()] == ["ativo"]
    assert [i.nome for i in banco.session.scalars(db.select(ItemTeste))] == ["ativo"]
    assert ItemTeste.query.filter_by(nome="excluido").first() is None


# 3b. ...e aparece na consulta explícita (continua no banco)
def test_excluido_aparece_na_consulta_explicita(banco):
    admin = _preparar(banco)

    todos = ItemTeste.query.execution_options(**{INCLUIR_EXCLUIDOS: True}).order_by(ItemTeste.nome).all()
    assert [i.nome for i in todos] == ["ativo", "excluido"]
    excluido = todos[1]
    assert excluido.excluido is True
    assert excluido.deleted_at is not None
    assert excluido.deleted_by == admin.id
    assert excluido.exclusao_id is not None


def test_itens_excluidos_juntos_compartilham_exclusao_id(banco):
    admin = Usuario(nome="Admin", email="admin@ifpb.edu.br", perfil=Perfil.ADMINISTRADOR)
    admin.definir_senha("Segredo123")
    sala, equipamento = ItemTeste(nome="sala"), ItemTeste(nome="equipamento")
    banco.session.add_all([admin, sala, equipamento])
    banco.session.commit()

    id_da_exclusao = sala.excluir(admin)
    equipamento.excluir(admin, exclusao_id=id_da_exclusao)
    banco.session.commit()

    assert sala.exclusao_id == equipamento.exclusao_id
    assert ItemTeste.query.count() == 0
