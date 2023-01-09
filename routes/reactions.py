import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import User
from routes.auth import get_current_user_from_token
from schemas.reactions import ReactionIn, verify_input_reaction

router = APIRouter(prefix="/reactions", tags=['reactions'])

logger = logging.getLogger(__name__)

@router.post('/set')
async def set_reaction(reaction: ReactionIn, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user_from_token)):
    if not verify_input_reaction(reaction):
        raise HTTPException(status_code=400, detail='Invalid reaction parameters!')
    return {'code': 200}

