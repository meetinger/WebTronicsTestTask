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
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    """Схема токена"""
    access_token: str
    refresh_token: str | None
    token_type: str
