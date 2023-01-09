from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import declared_attr, declarative_mixin, relationship

# from db.models import Reaction

import db.models.reactions_models as reaction_models

REACTION_CLASS = reaction_models.Reaction

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