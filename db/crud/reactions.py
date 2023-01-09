from sqlalchemy.orm import Session

from db.models import User
from db.models.reactions import Reaction
from schemas.reactions import ReactionIn, ReactionTypes, ReactionEntities


def create_reaction(reaction: ReactionIn, db: Session, current_user: User):
    reaction_db = Reaction(type=ReactionTypes[reaction.reaction_type])
    entity_db = ReactionEntities[reaction.entity_type]
