from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    """Класс пользователя"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    user_posts = relationship('Post', back_populates='user')
    user_reactions = relationship('Reaction', back_populates='user')
