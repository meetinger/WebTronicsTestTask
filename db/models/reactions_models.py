from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.database import Base


class Reaction(Base):
    """Класс реакции"""
    __tablename__ = 'reactions'


    id = Column(Integer, primary_key=True, index=True)
    type = Column(Integer, index=True)

    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship('User', back_populates='user_reactions')

    # тут ещё FK для остальных сущностей, см. db.models.mixins.ReactionsFKMixin