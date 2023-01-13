import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.crud.reactions_cruds import create_reaction, update_reaction, delete_reaction
from db.database import get_db
from db.models import User, Reaction
from routes.auth_routes import get_current_user_from_token
from schemas.reactions_schemas import ReactionIn, verify_input_reaction, get_reaction_entity_type, \
    get_reaction_entity_id_column, ReactionData, ReactionTypes, ReactionOut

router = APIRouter(prefix="/reactions", tags=['reactions'])

logger = logging.getLogger(__name__)


@router.post('/set', response_model=ReactionOut)
async def set_reaction(reaction: ReactionIn, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user_from_token)):
    """Эндпоинт для установки реакций"""
    if not verify_input_reaction(reaction):
        raise HTTPException(status_code=400, detail='Invalid reaction parameters!')

    entity_type = get_reaction_entity_type(clsname=reaction.entity_type)

    entity_db = db.query(entity_type).filter_by(id=reaction.entity_id).first()
    if entity_db is None:
        raise HTTPException(status_code=404, detail='Entity not found!')

    if entity_db.user_id == current_user.id:
        raise HTTPException(status_code=409, detail=f'You can not put a reaction on your {reaction.entity_type}!')

    entity_id_column = get_reaction_entity_id_column(clsname=reaction.entity_type)

    reaction_data = ReactionData(entity_id_column=entity_id_column, entity=entity_db,
                                 reaction_type=ReactionTypes[reaction.reaction_type].value, reaction_db=None)

    reaction_filter_kwargs = {
        reaction_data.entity_id_column.name: entity_db.id,
        'user_id': current_user.id
    }

    reaction_db = db.query(Reaction).filter_by(**reaction_filter_kwargs).first()

    if reaction_db is None:
        if reaction.reaction_type == 'unset':
            raise HTTPException(status_code=404, detail='Reaction not found!')
        reaction_db = create_reaction(reaction_data=reaction_data, db=db, current_user=current_user)
    else:
        if reaction.reaction_type == 'unset':
            delete_reaction(reaction_id=reaction_db.id, reaction_data=reaction_data, db=db,
                            current_user=current_user)
            return ReactionOut(reaction_type=reaction.reaction_type, entity_id=reaction.entity_id,
                               entity_type=reaction.entity_type)
        if ReactionTypes[reaction.reaction_type].value == reaction_db.type:
            raise HTTPException(status_code=409, detail='Reaction with current parameters already set!')
        reaction_data.reaction_db = reaction_db

        reaction_db = update_reaction(reaction_id=reaction_db.id, reaction_data=reaction_data, db=db,
                                      current_user=current_user)
    return ReactionOut(id=reaction_db.id, reaction_type=reaction.reaction_type, entity_id=reaction.entity_id,
                       entity_type=reaction.entity_type)
