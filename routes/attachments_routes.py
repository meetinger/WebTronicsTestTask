import logging
import os.path
import core.utils.attachments as attachment_utils
import routes.docs_examples.attachments_routes_examples as attachment_routes_examples

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from db.crud.attachments_cruds import get_attachment_by_filename
from db.database import get_db

router = APIRouter(prefix="/attachments", tags=['auxiliary'])

logger = logging.getLogger(__name__)

@router.get('/view/{filename}', responses=attachment_routes_examples.view_attachment_responses_examples, response_class=FileResponse)
async def view(filename: str = Path(description='Имя файла вложения'), db: Session = Depends(get_db)):
    """Получить файл вложения"""
    attachment_db = get_attachment_by_filename(filename=filename, db=db)
    not_found_exception = HTTPException(status_code=404, detail='Attachment not found')
    if attachment_db is None:
        raise not_found_exception
    file_path = attachment_utils.get_file_path(attachment_db.filename)
    if not os.path.exists(file_path):
        logger.warning(msg=f'Attachment in DB found, but file path not exist!\n{attachment_db}')
        raise not_found_exception
    return FileResponse(file_path)
