import urllib.parse

from fastapi import APIRouter, Body, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/urlparser", tags=['auxiliary'])


class RawURL(BaseModel):
    url: str = Field(description="Оригинальный URL")

    class Config:
        schema_extra = {
            'example': {
                'url': 'http://example.com/?q=search'
            }
        }


class EncodedURL(BaseModel):
    encoded_url: str = Field(description="Закодированный URL")

    class Config:
        schema_extra = {
            'example': {
                'encoded_url': 'http%3A//example.com/%3Fq%3Dsearch'
            }
        }


def decode_url(url: str) -> str:
    return urllib.parse.unquote(url)


def encode_url(url: str) -> str:
    return urllib.parse.quote(url)


@router.get('/encode_url/', response_model=EncodedURL)
async def encode_url_query(url: str = Query(description='Ссылка, которую нужно закодировать', example='http://example.com/?q=search')):
    return EncodedURL(encoded_url=encode_url(decode_url(url)))


@router.post('/encode_url', response_model=EncodedURL)
async def encode_url_post(url: RawURL = Body(description='Ссылка, которую нужно закодировать')):
    return EncodedURL(encoded_url=encode_url(decode_url(url.url)))
