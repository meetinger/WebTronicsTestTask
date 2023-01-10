from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from core.utils.attachments import get_view_url
from core.utils.serialization import sqlalchemy_to_pydantic_or_dict
from db.database import get_db
from db.models import User, Post
from routes.auth_routes import get_current_user_from_token
from schemas.posts_schemas import PostOut
from schemas.users_schemas import UserOut, UserLimited

router = APIRouter(prefix="/users", tags=['users'])


@router.get('/info', response_model=UserOut)
async def info_current_user(current_user: User = Depends(get_current_user_from_token)):
    return sqlalchemy_to_pydantic_or_dict(UserOut, current_user)


@router.get('/{user_id}/info', response_model=UserOut | UserLimited)
async def info_user_by_id(user_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user_from_token)):
    """Получение информации о пользователе"""
    if user_id is None or user_id == current_user.id:
        return sqlalchemy_to_pydantic_or_dict(UserOut, current_user)
    user_db = db.query(User).filter_by(id=user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail='User not found')
    return sqlalchemy_to_pydantic_or_dict(UserLimited, user_db)


@router.get('/{user_id}/posts', response_model=list[PostOut])
async def user_posts(user_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user_from_token)):
    posts_db = db.query(Post).filter_by(user_id=user_id).all()
    posts_out = [PostOut(id=post_db.id, text=post_db.text,
                         attachments_urls=[get_view_url(attachment.filename) for attachment in post_db.attachments]) for
                 post_db in posts_db]
    return posts_out
