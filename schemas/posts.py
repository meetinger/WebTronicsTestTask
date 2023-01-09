from pydantic import BaseModel


class PostBase(BaseModel):
    """Базовая схема поста"""
    text: str


class PostIn(PostBase):
    """Схема поста которая приходит от клиентов"""
    pass
    # attachments: list[bytes] | None


class PostOut(PostBase):
    """Схема поста которая уходит клиентам"""
    id: int
    attachments_urls: list[str] | None
    class Config:
        orm_mode = True

