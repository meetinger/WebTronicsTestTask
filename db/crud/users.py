import sqlalchemy
from sqlalchemy.orm import Session

from core.security import PasswordUtils
from db.models.users import User
from schemas.users import UserIn


def create_new_user(user: UserIn, db: Session) -> sqlalchemy.orm.query.Query:
    """Создание пользователя"""
    user = User(username=user.username,
                email=user.email,
                hashed_password=PasswordUtils.hash_password(user.password),
                )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(username: str, db: Session) -> sqlalchemy.orm.query.Query:
    """Получить пользователя по юзернейму"""
    return db.query(User).filter_by(username=username).first()
