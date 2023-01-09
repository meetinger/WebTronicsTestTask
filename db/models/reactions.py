import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from db.database import Base
from schemas.reactions import ReactionTypes

class Reaction(Base):
    """Класс реакции"""
    __tablename__ = 'reactions'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ReactionTypes), index=True)

    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship('User', back_populates='user_reactions')

    # тут ещё FK для остальных сущностей, см. db.models.mixins.ReactionsFKMixin
