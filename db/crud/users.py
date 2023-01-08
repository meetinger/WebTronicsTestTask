from sqlalchemy.orm import Session

from core.security import PasswordUtils
from db.models.users import User
from schemas.users import UserIn


def create_new_user(user: UserIn, db: Session):
    """Создание пользователя"""
    user = User(username=user.username,
                email=user.email,
                hashed_password=PasswordUtils.hash_password(user.password),
                )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

