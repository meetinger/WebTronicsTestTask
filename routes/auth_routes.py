import logging

import sqlalchemy
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import ExpiredSignatureError
from sqlalchemy.orm import Session

from core.security import PasswordUtils, TokenUtils
from db.crud.users_crud import create_new_user, get_user
from db.database import get_db
from db.models.users_models import User
from schemas.users_schemas import UserOut, UserIn, Token

router = APIRouter(prefix="/auth", tags=['auth'])

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/get_token")


def get_current_user_from_token(token: str = Depends(oauth2_scheme),
                                db: Session = Depends(get_db)) -> sqlalchemy.orm.query.Query:
    """Получение юзера из токена"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try:
        payload = TokenUtils.decode_token(token)
        username = payload['sub']
    except ExpiredSignatureError:
        logger.error(msg='Token expired')
        raise HTTPException(status_code=403, detail='Token expired')
    except Exception as e:
        logger.error(msg='Error while getting user from token', exc_info=e)
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


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
    return create_new_user(user=user, db=db)


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
        tokens = TokenUtils.create_token_pair({'sub': user.username})
        return tokens
    except Exception as e:
        logger.error('Error while token pair generation', exc_info=e)
