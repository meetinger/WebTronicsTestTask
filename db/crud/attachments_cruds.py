from fastapi import UploadFile
from sqlalchemy.orm import Session

import core.utils.attachments as attachment_utils
from db.models import Attachment


def create_attachments(upload_files: [UploadFile], db: Session, save_to_db=True) -> list[Attachment]:
    """Создать вложения"""
    def _create_attachment(upload_file: UploadFile):
        """Внутренняя функция создания вложения"""
        filename = attachment_utils.gen_filename(upload_file.content_type)
        while db.query(Attachment.id).filter_by(filename=filename).first() is not None:
            filename = attachment_utils.gen_filename(upload_file.content_type)
        attachment_utils.save_file(filename=filename, file_bytes=upload_file.file.read())

        return Attachment(filename=filename, original_filename=upload_file.filename)

    attachments_db = [_create_attachment(i) for i in upload_files]

    if save_to_db:
        db.bulk_save_objects(attachments_db)
        db.commit()
        db.refresh(attachments_db)

    return attachments_db


def get_attachment_by_filename(filename: str, db: Session) -> Attachment:
    """Получить вложение"""
    return db.query(Attachment).filter_by(filename=filename).first()


def delete_attachments(attachment_ids: list[int], db: Session, save_to_db=True) -> bool:
    """Удалить вложения"""
    attachments = db.query(Attachment).filter(Attachment.id.in_(attachment_ids))
    for attachment in attachments:
        attachment_utils.delete_file(attachment.filename)
    attachments.delete()
    if save_to_db:
        db.commit()
    return True

