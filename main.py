from logging.config import dictConfig

from fastapi import FastAPI

from core.settings import settings
from routes import auth_routes, posts_routes, attachments_routes, users_routes, reactions_routes

dictConfig(settings.LOGGER_CONFIG)

app = FastAPI()
app.include_router(auth_routes.router)
app.include_router(posts_routes.router)
app.include_router(attachments_routes.router)
app.include_router(users_routes.router)
app.include_router(reactions_routes.router)


if __name__ == '__main__':
    pass