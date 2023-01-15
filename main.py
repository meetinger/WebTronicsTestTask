from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI

from core.settings import settings
from routes import auth_routes, posts_routes, attachments_routes, users_routes, reactions_routes

dictConfig(settings.LOGGER_CONFIG)

tags_metadata = [
    {
        "name": "auth",
        "description": "Регистрация и аутентификация"
    },
    {
        "name": "posts",
        "description": "Операции с постами"
    },
    {
        "name": "auxiliary",
        "description": "Вспомогательные методы для различных операций"
    },
    {
        "name": "users",
        "description": "Получение пользовательской информации"
    },
    {
        "name": "reactions",
        "description": "Операции с реакциями"
    },
]

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(auth_routes.router)
app.include_router(posts_routes.router)
app.include_router(attachments_routes.router)
app.include_router(users_routes.router)
app.include_router(reactions_routes.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)