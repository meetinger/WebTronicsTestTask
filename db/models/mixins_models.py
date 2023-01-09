import enum
from typing import Type

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, declarative_mixin, declared_attr

from db.models.reactions_models import Reaction

REACTION_CLASS = Reaction

@declarative_mixin
class ReactionsFKMixin:
    """Примесь для автоматической вставки FK для реакций"""

    @declared_attr
    def reactions(cls):
        entity_name = cls.__name__.lower()

        ref_id = Column(Integer, ForeignKey(f'{cls.__tablename__}.id'), index=True)
        ref = relationship(cls.__name__, back_populates='reactions')
        setattr(REACTION_CLASS, f'{entity_name}_id', ref_id)
        setattr(REACTION_CLASS, entity_name, ref)

        return relationship('Reaction', back_populates=entity_name)

def get_reactions_entities_types() -> Type[enum.Enum]:
    """Функция получения enum сущностей, поддерживающих реакцию"""
    enum_cls = enum.Enum('ReactionEntities', {subcls.__name__: subcls for subcls in ReactionsFKMixin.__subclasses__()})
    return enum_cls
