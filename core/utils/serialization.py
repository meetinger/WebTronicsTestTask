from typing import Type

from pydantic import BaseModel

from db.database import Base


def sqlalchemy_to_pydantic(pydantic_cls: Type[BaseModel], sqlalchemy_obj: Base):
    """Преобразование модели SqlAlchemy в модель Pydantic"""
    data_dct = {key: getattr(sqlalchemy_obj, key) for key in pydantic_cls.__fields__.keys()}
    return pydantic_cls(**data_dct)
