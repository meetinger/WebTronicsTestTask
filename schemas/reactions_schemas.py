import enum
from dataclasses import dataclass

from pydantic import BaseModel
from sqlalchemy import Column

from db.database import Base
from db.models import Reaction
from db.models.mixins_models import get_reactions_entities_types

# enum с сущностями, поддерживающими реакции
ReactionEntities = get_reactions_entities_types()


class ReactionTypes(enum.Enum):
    """Типы реакций"""
    unset = 0
    like = 1
    dislike = 2


class ReactionIn(BaseModel):
    """Схема реакции"""
    entity_type: str
    entity_id: int
    reaction_type: str


@dataclass
class ReactionData:
    entity_id_column: Column
    entity: Base
    reaction_type: int
    reaction_db: Reaction | None


class ReactionOut(BaseModel):
    id: int | None
    reaction_type: str
    entity_id: int
    entity_type: str

    # class Config:
    #     orm_mode = True


def verify_input_reaction(reaction: ReactionIn) -> bool:
    """Проверка корректности аттрибутов реакции"""
    return hasattr(ReactionEntities, reaction.entity_type) and hasattr(ReactionTypes, reaction.reaction_type)


def get_reaction_entity_type(clsname: str) -> Base:
    """Получить модель сущности по имени типа сущности"""
    return getattr(ReactionEntities, clsname).value


def get_reaction_entity_id_column(clsname: str):
    """Получить orm-столбец из реакции имени типа сущности"""
    return getattr(Reaction, f'{clsname}_id')
