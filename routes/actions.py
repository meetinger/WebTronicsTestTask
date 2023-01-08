import logging

from fastapi import APIRouter

router = APIRouter(prefix="/actions", tags=['actions'])

logger = logging.getLogger(__name__)

@router.post('/create')
async def create_post():
    pass