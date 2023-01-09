from pydantic import EmailStr, BaseModel


class UserBase(BaseModel):
    username: str
    name: str


class UserFull(UserBase):
    """Полная схема пользователя"""
    id: int
    email: EmailStr


class UserIn(UserBase):
    """Схема пользователя которая приходит от клиентов"""
    email: EmailStr
    password: str


class UserOut(UserFull):
    """Схема пользователя которая уходит клиентам"""

    class Config:
        orm_mode = True

class UserLimited(UserBase):
    """Схема пользователя скрывающая email"""
    id: int


class Token(BaseModel):
    """Схема токена"""
    access_token: str
    refresh_token: str | None
    token_type: str
