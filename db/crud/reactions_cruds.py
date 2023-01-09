from sqlalchemy.orm import Session

from db.models import Reaction
from db.models import User
from schemas.reactions_schemas import ReactionIn, ReactionTypes, ReactionEntities


def create_reaction(reaction: ReactionIn, db: Session, current_user: User):
    reaction_db = Reaction(type=ReactionTypes[reaction.reaction_type])
    entity_db = ReactionEntities[reaction.entity_type]
