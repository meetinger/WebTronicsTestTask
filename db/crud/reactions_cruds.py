from sqlalchemy.orm import Session

from db.database import Base
from db.models import Reaction
from db.models import User
from db.models.mixins_models import get_reactions_entities_types
from schemas.reactions_schemas import ReactionBase, ReactionTypes, ReactionEntities, ReactionData, \
    get_reaction_entity_id_column


def create_reaction(reaction_data: ReactionData, db: Session, current_user: User) -> Reaction:
    reaction_kwargs = {'type': reaction_data.reaction_type,
                       'user_id': current_user.id,
                       reaction_data.entity_id_column.name: reaction_data.entity.id
                       }
    reaction_db = Reaction(**reaction_kwargs)
    db.add(reaction_db)
    db.commit()
    db.refresh(reaction_db)
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
    db.refresh(reaction_db)
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


def get_reactions_count_for_entity(entity_db: Base, db: Session):
    entity_cls = entity_db.__class__
    entity_clsname = entity_cls.__name__.lower()
    reaction_entity_id_column = get_reaction_entity_id_column(entity_clsname)

    reaction_types_dict = {i.name: i.value for i in ReactionTypes if i.name != 'unset'}

    reactions_count_dict = {key: db.query(Reaction.id).filter_by(
                                    **{reaction_entity_id_column.name: value}).count()
                            for key, value in reaction_types_dict.items()}

    return reactions_count_dict
