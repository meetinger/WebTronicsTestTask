import sqlalchemy
from sqlalchemy.orm import Session

from core.security import PasswordUtils
from db.models.users import User
from schemas.users import UserIn


def create_new_user(user: UserIn, db: Session) -> sqlalchemy.orm.query.Query:
    """Создание пользователя"""
    user_db = User(username=user.username,
                email=user.email,
                hashed_password=PasswordUtils.hash_password(user.password),
                )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def get_user(username: str, db: Session) -> sqlalchemy.orm.query.Query:
    """Получить пользователя по юзернейму"""
    return db.query(User).filter_by(username=username).first()
