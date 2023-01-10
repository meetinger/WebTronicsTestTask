from sqlalchemy.orm import Session

from db.models import Reaction
from db.models import User
from schemas.reactions_schemas import ReactionIn, ReactionTypes, ReactionEntities, ReactionData


def create_reaction(reaction_data: ReactionData, db: Session, current_user: User) -> Reaction:
    reaction_kwargs = {'type': reaction_data.reaction_type,
                       'user_id': current_user.id,
                       reaction_data.entity_id_column.name: reaction_data.entity.id
                       }
    reaction_db = Reaction(**reaction_kwargs)
    db.add(reaction_db)
    db.commit()
    return reaction_db

def update_reaction(reaction_id: int, reaction_data: ReactionData, db: Session, current_user: User) -> Reaction:
    reaction_db = reaction_data.reaction_db
    if reaction_db is None:
        reaction_db = db.query(Reaction).filter_by(id=reaction_id).first()
    if reaction_db is None:
        raise ValueError('Reaction not found!')
    reaction_db.type = reaction_data.reaction_type
    db.add(reaction_db)
    db.commit()
    return reaction_db


def delete_reaction(reaction_id: int, reaction_data, db: Session, current_user: User) -> bool:
    reaction_db = reaction_data.reaction_db
    if reaction_db is None:
        reaction_db = db.query(Reaction).filter_by(id=reaction_id).first()
    if reaction_db is None:
        raise ValueError('Reaction not found!')
    db.delete(reaction_db)
    db.commit()
    return True
