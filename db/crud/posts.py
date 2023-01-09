import sqlalchemy
import core.utils.attachments as attachment_utils

from fastapi import UploadFile, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Post, User, Attachment
from schemas.posts import PostIn


def create_new_post(text: str, attachments: list[UploadFile], current_user: User,
                    db: Session) -> sqlalchemy.orm.query.Query:
    """Создать новый пост"""

    def _create_attachment_obj(upload_file: UploadFile) -> Attachment:
        """Внутренняя функция создания объекта вложения"""

        filename = attachment_utils.gen_filename(upload_file.content_type)
        while db.query(Attachment.id).filter_by(filename=filename).first() is not None:
            filename = attachment_utils.gen_filename(upload_file.content_type)
        attachment_utils.save_file(filename=filename, file_bytes=upload_file.file.read())

        return Attachment(filename=filename)

    post_db = Post(text=text, user_id=current_user.id)
    attachments_db = [_create_attachment_obj(upload_file=i) for i in attachments]
    post_db.attachments.extend(attachments_db)
    db.add(post_db)
    db.commit()
    return post_db


def get_attachment(filename: str, db: Session) -> sqlalchemy.orm.query.Query:
    """Получить вложение"""
    return db.query(Attachment).filter_by(filename=filename).first()
