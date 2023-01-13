from sqlalchemy.orm import Session

from core.security import PasswordUtils
from db.models.users_models import User
from schemas.users_schemas import UserIn


def create_new_user(user: UserIn, db: Session) -> User:
    """Создание пользователя"""
    user_db = User(username=user.username,
                   name=user.name,
                   email=user.email,
                   hashed_password=PasswordUtils.hash_password(user.password),
                  )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def get_user(username: str, db: Session) -> User:
    """Получить пользователя по юзернейму"""
    return db.query(User).filter_by(username=username).first()
