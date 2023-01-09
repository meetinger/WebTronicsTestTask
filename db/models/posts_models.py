from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base
from db.models.mixins_models import ReactionsFKMixin


class Post(Base, ReactionsFKMixin):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)

    user = relationship('User', back_populates='user_posts')
    attachments = relationship('Attachment', back_populates='post')

