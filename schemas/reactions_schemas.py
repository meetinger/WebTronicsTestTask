import enum
from dataclasses import dataclass

from pydantic import BaseModel, Field
from sqlalchemy import Column

from db.database import Base
from db.models import Reaction
from db.models.mixins_models import get_reactions_entities_types

# enum с сущностями, поддерживающими реакции
ReactionEntities = enum.Enum('ReactionEntities', get_reactions_entities_types())


class ReactionTypes(enum.Enum):
    """Типы реакций"""
    unset = 0
    like = 1
    dislike = 2


class ReactionBase(BaseModel):
    """Схема реакции"""
    entity_type: str = Field(
        description=f'Тип сущности. Доступные варианты: {", ".join(get_reactions_entities_types().keys())}')
    entity_id: int = Field(description='id сущности, на которой реакция')
    reaction_type: str = Field(
        description=f'Тип реакции. Доступные варианты: {", ".join(i.name for i in ReactionTypes)}')

class ReactionOut(ReactionBase):
    user_id: int = Field(description='id пользователя, который поставил реакцию')


@dataclass
class ReactionData:
    entity_id_column: Column
    entity: Base
    reaction_type: int
    reaction_db: Reaction | None


def verify_input_reaction(reaction: ReactionBase) -> bool:
    """Проверка корректности аттрибутов реакции"""
    return hasattr(ReactionEntities, reaction.entity_type) and hasattr(ReactionTypes, reaction.reaction_type)


def get_reaction_entity_type(clsname: str) -> Base:
    """Получить модель сущности по имени типа сущности"""
    return getattr(ReactionEntities, clsname).value


def get_reaction_entity_id_column(clsname: str):
    """Получить orm-столбец из реакции имени типа сущности"""
    return getattr(Reaction, f'{clsname}_id')
