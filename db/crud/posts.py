import sqlalchemy
import core.utils.attachments as attachment_utils

from fastapi import UploadFile
from sqlalchemy.orm import Session

from db.crud.attachments import create_attachments, delete_attachments
from db.models import Post, User, Attachment


def create_new_post(text: str, attachments: list[UploadFile], current_user: User,
                    db: Session) -> Post:
    """Создать новый пост"""

    post_db = Post(text=text, user_id=current_user.id)
    attachments_db = create_attachments(upload_files=attachments, db=db, save_to_db=False)
    post_db.attachments.extend(attachments_db)
    db.add(post_db)
    db.commit()
    return post_db

def get_post(post_id: int, db: Session) -> Post:
    """Получить пост"""
    return db.query(Post).filter_by(id=post_id).first()

def delete_post(post_id: int, db: Session) -> bool:
    """Удалить пост"""
    db.query(Post).filter_by(id=post_id).delete()
    db.commit()
    return True

def update_post(post_id: int, text: str, attachments: list[UploadFile], db: Session) -> Post:
    """Обновить пост"""
    post_db = db.query(Post).filter_by(id=post_id).first()
    if post_db is None:
        raise ValueError('Post not found!')
    post_db.text = text
    delete_attachments(attachment_ids=[i.id for i in post_db.attachments], db=db, save_to_db=False)
    post_db.attachments = create_attachments(upload_files=attachments, db=db, save_to_db=False)
    db.commit()
    return post_db

