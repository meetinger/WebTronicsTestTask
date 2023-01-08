from pydantic import EmailStr, BaseModel


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    username: str
    email: EmailStr


class UserIn(UserBase):
    """Схема пользователя которая приходит от клиентов"""
    password: str


class UserOut(UserBase):
    """Схема пользователя которая уходит клиентам"""
    pass
