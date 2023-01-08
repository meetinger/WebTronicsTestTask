import logging

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from core.utils.serialization import sqlalchemy_to_pydantic
from db.crud.users import create_new_user
from db.database import get_db
from db.models import User
from schemas.users import UserOut, UserIn

router = APIRouter(prefix="/auth", tags=['auth'])

logger = logging.getLogger(__name__)


@router.post('/register')
async def register(user: UserIn, db: Session = Depends(get_db)):
    """Эндпоинт регистрации пользователя"""
    if db.query(User.id).filter_by(email=user.email).first() is not None:
        e = HTTPException(status_code=409, detail='This email already exist!')
        logger.debug(msg='This email already exist!', exc_info=e)
        return e
    if db.query(User.id).filter_by(username=user.username).first() is not None:
        e = HTTPException(status_code=409, detail='This username already exist!')
        logger.debug(msg='This username already exist!', exc_info=e)
        return e
    try:
        return sqlalchemy_to_pydantic(UserOut, create_new_user(user=user, db=db))
    except Exception as e:
        logger.error(msg='Error Insert in to DB', exc_info=e)
        return HTTPException(status_code=500, detail=f'Internal Server Error: {e}', )

