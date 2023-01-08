from logging.config import dictConfig
import logging

from fastapi import FastAPI

from core.settings import settings
from routes import auth

dictConfig(settings.LOGGER_CONFIG)

app = FastAPI()
app.include_router(auth.router)


if __name__ == '__main__':
    pass