"""Exclusão lógica (SPEC-01 RN-002): itens "excluídos" ficam no banco, mas somem das consultas.

Como usar num modelo:

    class Sala(ExclusaoLogicaMixin, db.Model):
        ...

- `sala.excluir(autor)` marca a sala como excluída (não apaga a linha).
- Toda consulta comum (`Sala.query...`, `db.select(Sala)`) traz só os itens NÃO excluídos.
- Para ver também os excluídos, peça explicitamente:
      Sala.query.execution_options(incluir_excluidos=True).all()
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import event, orm
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db

INCLUIR_EXCLUIDOS = "incluir_excluidos"


class ExclusaoLogicaMixin:
    """Acrescenta deleted_at, deleted_by e exclusao_id ao modelo (PLAN §2)."""

    @orm.declared_attr
    def deleted_at(cls):
        return db.Column(db.DateTime(timezone=True), nullable=True)

    @orm.declared_attr
    def deleted_by(cls):
        return db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)

    # Mesmo id para tudo que foi excluído junto (ex.: sala + seus equipamentos),
    # preparando a futura restauração (fora do MVP).
    @orm.declared_attr
    def exclusao_id(cls):
        return db.Column(UUID(as_uuid=True), nullable=True, index=True)

    @property
    def excluido(self):
        return self.deleted_at is not None

    def excluir(self, autor, exclusao_id=None):
        """Marca como excluído. Não faz commit (quem chama grava junto com o log)."""
        self.deleted_at = datetime.now(timezone.utc)
        self.deleted_by = autor.id
        self.exclusao_id = exclusao_id or uuid.uuid4()
        return self.exclusao_id


@event.listens_for(orm.Session, "do_orm_execute")
def _esconder_excluidos(estado):
    """Filtro padrão: acrescenta `deleted_at IS NULL` a toda consulta, salvo pedido explícito."""
    if (
        estado.is_select
        and not estado.is_column_load
        and not estado.is_relationship_load
        and not estado.execution_options.get(INCLUIR_EXCLUIDOS, False)
    ):
        estado.statement = estado.statement.options(
            orm.with_loader_criteria(
                ExclusaoLogicaMixin,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )
