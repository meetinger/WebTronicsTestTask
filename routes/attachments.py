import logging
import core.utils.attachments as attachment_utils

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from db.crud.posts import get_attachment
from db.database import get_db

router = APIRouter(prefix="/attachments", tags=['auxiliary'])

logger = logging.getLogger(__name__)

@router.get('/get/{filename}')
async def get_file(filename: str, db: Session = Depends(get_db)):
    attachment_db = get_attachment(filename=filename, db=db)
    if attachment_db is None:
        raise HTTPException(status_code=404, detail='Attachment not found')
    # file = attachment_utils.get_attachment_file(attachment_db.filename)
    file_path = attachment_utils.get_file_path(attachment_db.filename)
    return FileResponse(file_path)