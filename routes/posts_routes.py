import logging
import routes.docs_examples.posts_examples as posts_examples

from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException, Body, Query, Path
from sqlalchemy.orm import Session

from core.utils.attachments import get_view_url
from db.crud.posts_cruds import create_new_post, get_post, update_post
from db.crud.reactions_cruds import get_reactions_count_for_entity
from db.database import get_db
from db.models import User, Post
from routes.auth_routes import get_current_user_from_token
from schemas.posts_schemas import PostOut
from schemas.reactions_schemas import ReactionTypes

router = APIRouter(prefix="/posts", tags=['posts'])

logger = logging.getLogger(__name__)


@router.post('/create', response_model=PostOut, responses=posts_examples.create_post_responses_examples)
async def create_post(attachments: list[UploadFile] = Form(default=[], description="Вложения к посту"),
                      text: str = Form(description="Текст поста"),
                      current_user: User = Depends(get_current_user_from_token),
                      db: Session = Depends(get_db)):
    """Создать пост"""
    post_db = create_new_post(text=text, attachments=attachments, current_user=current_user, db=db)
    post_out = PostOut(id=post_db.id, text=post_db.text,
                       reactions_count=None, user_id=post_db.user_id,
                       attachments_urls=[get_view_url(attachment.filename) for attachment in post_db.attachments])
    return post_out


@router.get('/view/{post_id}', response_model=PostOut, responses=posts_examples.view_post_responses_examples)
async def view_post(post_id: int = Path(description="id поста"), db: Session = Depends(get_db)):
    """Посмотреть пост"""
    post_db = get_post(post_id=post_id, db=db)
    if post_db is None:
        return HTTPException(status_code=404, detail='Post not found')
    reactions_count_dict = get_reactions_count_for_entity(entity_db=post_db, db=db)
    post_out = PostOut(id=post_db.id, text=post_db.text, reactions_count=reactions_count_dict, user_id=post_db.user_id,
                       attachments_urls=[get_view_url(attachment.filename) for attachment in post_db.attachments])
    return post_out


@router.put('/edit/{post_id}', response_model=PostOut, responses=posts_examples.edit_post_responses_examples)
async def edit_post(post_id: int = Path(description="id поста"),
                    attachments: list[UploadFile] = Form(default=[], description="Вложения к посту"),
                    text: str = Form(description="Текст поста"),
                    current_user: User = Depends(get_current_user_from_token),
                    db: Session = Depends(get_db)):
    """Отредактировать пост"""
    if attachments is None:
        attachments = []
    post_user_id = db.query(Post.user_id).filter_by(id=post_id).first()[0]
    if post_user_id is None:
        return HTTPException(status_code=404, detail='Post not found')
    if post_user_id != current_user.id:
        raise HTTPException(status_code=403, detail='This post was created by another user!')
    post_db = update_post(post_id=post_id, text=text, attachments=attachments, db=db)
    reactions_count_dict = get_reactions_count_for_entity(entity_db=post_db, db=db)
    post_out = PostOut(id=post_db.id, text=post_db.text, reactions_count=reactions_count_dict, user_id=post_db.user_id,
                       attachments_urls=[get_view_url(attachment.filename) for attachment in post_db.attachments])
    return post_out
