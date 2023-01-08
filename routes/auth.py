import logging
from pprint import pprint

import sqlalchemy
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.security import PasswordUtils, TokenUtils
from core.utils.serialization import sqlalchemy_to_pydantic_or_dict
from db.crud.users import create_new_user, get_user
from db.database import get_db
from db.models import User
from schemas.users import UserOut, UserIn, Token

router = APIRouter(prefix="/auth", tags=['auth'])

logger = logging.getLogger(__name__)


def authenticate_user(username: str, password: str, db: Session) -> sqlalchemy.orm.query.Query | bool:
    """Аутентификация пользователя"""
    user = get_user(username=username, db=db)
    if not user:
        return False
    if not PasswordUtils.verify_password(password, user.hashed_password):
        return False
    return user


@router.post('/register', response_model=UserOut)
async def register(user: UserIn, db: Session = Depends(get_db)):
    """Эндпоинт регистрации пользователя"""
    if db.query(User.id).filter_by(email=user.email).first() is not None:
        e = HTTPException(status_code=409, detail='This email already exist!')
        logger.debug(msg='This email already exist!', exc_info=e)
        raise e
    if db.query(User.id).filter_by(username=user.username).first() is not None:
        e = HTTPException(status_code=409, detail='This username already exist!')
        logger.debug(msg='This username already exist!', exc_info=e)
        raise e
    try:
        return create_new_user(user=user, db=db)
    except Exception as e:
        logger.error(msg='Error Insert in to DB', exc_info=e)
        raise HTTPException(status_code=500, detail=f'Internal Server Error: {e}', )

@router.post('/get_token', response_model=Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Получение пары токенов"""
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    try:
        tokens = TokenUtils.create_token_pair({'user': sqlalchemy_to_pydantic_or_dict(UserOut, user, to_dict=True)})
        pprint(tokens)
        return tokens
    except Exception as e:
        logger.error('Error while token pair generation', exc_info=e)

