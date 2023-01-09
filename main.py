import traceback
from logging.config import dictConfig

from fastapi import FastAPI
from starlette.requests import Request

from core.settings import settings
from routes import auth, actions, attachments

dictConfig(settings.LOGGER_CONFIG)

app = FastAPI()
app.include_router(auth.router)
app.include_router(actions.router)
app.include_router(attachments.router)


if __name__ == '__main__':
    pass