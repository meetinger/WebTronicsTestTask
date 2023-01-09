import enum

from pydantic import BaseModel

from db.models.mixins_models import get_reactions_entities_types


ReactionEntities = get_reactions_entities_types()

class ReactionTypes(enum.Enum):
    """Типы реакций"""
    empty = 0
    like = 1
    dislike = 2


class ReactionIn(BaseModel):
    """Схема реакции"""
    entity_type: str
    entity_id: int
    reaction_type: str


def verify_input_reaction(reaction: ReactionIn):
    """Проверка корректности аттрибутов реакции"""
    return hasattr(ReactionEntities, reaction.entity_type) and hasattr(ReactionTypes, reaction.reaction_type)