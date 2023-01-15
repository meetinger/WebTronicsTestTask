from pydantic import BaseModel, Field


class PostBase(BaseModel):
    """Базовая схема поста"""
    text: str = Field(description="Текст поста")

class PostOut(PostBase):
    """Схема поста которая уходит клиентам"""
    id: int = Field(description="id поста")
    attachments_urls: list[str] | list = Field(description="Массив с ссылками на вложения")
    reactions_count: dict | None = Field(description="JSON с количеством реакций")
    user_id: int = Field(description="id пользователя")
    class Config:
        orm_mode = True

