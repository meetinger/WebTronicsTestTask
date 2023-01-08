import logging

from fastapi import APIRouter

router = APIRouter(prefix="/attachments", tags=['actions'])

logger = logging.getLogger(__name__)

@router.get('get/{name}')
async def get_attachment(name: str):
    pass