import logging

from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session

from core.utils.attachments import get_view_url
from db.crud.posts_cruds import create_new_post, get_post, update_post
from db.database import get_db
from db.models import User, Post
from routes.auth_routes import get_current_user_from_token
from schemas.posts_schemas import PostOut

router = APIRouter(prefix="/posts", tags=['posts'])

logger = logging.getLogger(__name__)


@router.post('/create', response_model=PostOut)
async def create_post(attachments: list[UploadFile], text: str = Form(), current_user: User = Depends(get_current_user_from_token),
                      db: Session = Depends(get_db)):
    """Создать пост"""
    post_db = create_new_post(text=text, attachments=attachments, current_user=current_user, db=db)
    post_out = PostOut(id=post_db.id, text=post_db.text, attachments_urls=[get_view_url(attachment.filename) for attachment in post_db.attachments])
    return post_out

@router.get('/view/{post_id}', response_model=PostOut)
async def view_post(post_id: int, db: Session = Depends(get_db)):
    """Посмотреть пост"""
    post_db = get_post(post_id=post_id, db=db)
    post_out = PostOut(id=post_db.id, text=post_db.text,
                       attachments_urls=[get_view_url(attachment.filename) for attachment in post_db.attachments])
    return post_out

@router.put('/edit/{post_id}', response_model=PostOut)
async def edit_post(post_id: int, attachments: list[UploadFile], text: str = Form(), current_user: User = Depends(get_current_user_from_token),
                      db: Session = Depends(get_db)):
    """Отредактировать пост"""
    if db.query(Post.user_id).filter_by(id=post_id).first()[0] != current_user.id:
        raise HTTPException(status_code=403, detail='This post was created by another user!')
    post_db = update_post(post_id=post_id, text=text, attachments=attachments, db=db)
    post_out = PostOut(id=post_db.id, text=post_db.text,
                       attachments_urls=[get_view_url(attachment.filename) for attachment in post_db.attachments])
    return post_out
