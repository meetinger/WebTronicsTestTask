from logging.config import dictConfig

from fastapi import FastAPI

from core.settings import settings
from routes import auth, posts, attachments, users

dictConfig(settings.LOGGER_CONFIG)

app = FastAPI()
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(attachments.router)
app.include_router(users.router)


if __name__ == '__main__':
    pass