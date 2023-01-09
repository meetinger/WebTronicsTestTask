import enum
from typing import Type

from pydantic import BaseModel

from db.database import Base


def sqlalchemy_to_pydantic_or_dict(pydantic_cls: Type[BaseModel], sqlalchemy_obj: Base,
                                   to_dict: bool = False) -> BaseModel | dict:
    """Преобразование модели SqlAlchemy в модель Pydantic"""
    data_dct = {key: getattr(sqlalchemy_obj, key) for key in pydantic_cls.__fields__.keys()}
    return data_dct if to_dict else pydantic_cls(**data_dct)


def enum_to_dict(enum_cls: enum.Enum) -> dict:
    """Преобразование enum в dict"""
    return {i.name: i.value for i in enum_cls}