from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class Attachment(Base):
    """Модель вложения"""
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), index=True)

    post = relationship('Post', back_populates='attachments')
