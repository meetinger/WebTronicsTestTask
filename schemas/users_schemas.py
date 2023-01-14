from pydantic import EmailStr, BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(description='Username пользователя')
    name: str = Field(description='Имя пользователя')


class UserEmail(UserBase):
    email: EmailStr = Field(description='Email пользователя')


class UserFull(UserEmail):
    """Полная схема пользователя"""
    id: int = Field(description='id пользователя')


class UserIn(UserEmail):
    """Схема пользователя которая приходит от клиентов"""
    password: str = Field(description='Пароль пользователя')


class UserOut(UserFull):
    """Схема пользователя которая уходит клиентам"""

    class Config:
        orm_mode = True


class UserLimited(UserBase):
    """Схема пользователя скрывающая email"""
    id: int = Field(description='id пользователя')


class Token(BaseModel):
    """Схема токена"""
    access_token: str = Field(description='Access токен')
    refresh_token: str = Field(description='Refresh токен')
    token_type: str = Field(description='Тип токена(Bearer)')
