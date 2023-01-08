import logging
from pprint import pprint
from urllib.parse import urljoin

from fastapi import APIRouter, Depends, UploadFile, Form
from sqlalchemy.orm import Session

from core.settings import settings
from core.utils.attachments import get_view_url
from db.crud.posts import create_new_post
from db.database import get_db
from db.models import User
from routes.auth import get_current_user_from_token
from schemas.posts import PostIn, PostOut

router = APIRouter(prefix="/actions", tags=['actions'])

logger = logging.getLogger(__name__)


@router.post('/create_post', response_model=PostOut)
async def create_post(attachments: list[UploadFile], text: str = Form(), current_user: User = Depends(get_current_user_from_token),
                      db: Session = Depends(get_db)):
    post_db = create_new_post(text=text, attachments=attachments, current_user=current_user, db=db)
    post_out = PostOut(id=post_db.id, text=post_db.text, attachments_urls=[get_view_url(attachment.filename) for attachment in post_db.attachments])
    return post_out
