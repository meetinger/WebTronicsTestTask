import functools
import os
import pathlib

import pytest

import core.utils.attachments

from io import BytesIO
from pprint import pprint
from unittest.mock import patch

from typing import Generator, Any

from PIL import Image
from fastapi import FastAPI, UploadFile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.security import TokenUtils
from core.settings import settings
from db.crud.attachments_cruds import delete_attachments
from db.crud.posts_cruds import create_new_post
from db.crud.reactions_cruds import create_reaction
from db.crud.users_crud import create_new_user
from db.database import Base, get_db
from db.models import User, Post, Reaction
from routes import auth_routes, posts_routes, attachments_routes, users_routes, reactions_routes
from schemas.reactions_schemas import ReactionData, get_reaction_entity_id_column, ReactionTypes
from schemas.users_schemas import UserIn


def start_app() -> FastAPI:
    """Запуск приложения"""
    app = FastAPI()
    app.include_router(auth_routes.router)
    app.include_router(posts_routes.router)
    app.include_router(attachments_routes.router)
    app.include_router(users_routes.router)
    app.include_router(reactions_routes.router)
    return app


# тестовая БД
engine = create_engine(settings.DATABASE_TEST_URL)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """Создаём новую БД для каждого теста"""
    Base.metadata.create_all(engine)
    _app = start_app()
    yield _app
    Base.metadata.drop_all(engine)



@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    """Использование сессии в тестах"""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)

    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(monkeypatch, app: FastAPI, db_session: SessionTesting
           ) -> Generator[TestClient, Any, None]:
    """Клиент для тестирования"""

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    # перегрузка зависимостей
    app.dependency_overrides[get_db] = _get_test_db
    pathlib.Path(settings.POST_TEST_ATTACHMENTS_DIR).mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(core.utils.attachments, 'get_attachments_path', lambda: settings.POST_TEST_ATTACHMENTS_DIR)

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def user(db_session):
    def _user(user_in: UserIn) -> User:
        return create_new_user(user=user_in, db=db_session)

    return _user


@pytest.fixture(scope="function")
def user_token():
    def _user_token(user: User) -> dict:
        return TokenUtils.create_token_pair({'sub': user.username})

    return _user_token


@pytest.fixture(scope="function")
def post(db_session):
    attachments_db = []
    def _post(user: User, post_data: dict) -> Post:
        nonlocal attachments_db
        attachments = [UploadFile(*item) for _, item in post_data['attachments']]
        post_db = create_new_post(text=post_data['text'], attachments=attachments, current_user=user, db=db_session)
        attachments_db = post_db.attachments
        return post_db

    yield _post
    delete_attachments(attachment_ids=[a.id for a in attachments_db], db=db_session)


@pytest.fixture(scope="function")
def reaction(db_session):
    def _reaction(user: User, entity: Base, reaction_type: str) -> Reaction:
        reaction_data = ReactionData(entity_id_column=get_reaction_entity_id_column(clsname=entity.__class__.__name__),
                                     entity=entity,
                                     reaction_type=ReactionTypes[reaction_type].value, reaction_db=None)
        return create_reaction(reaction_data=reaction_data, db=db_session, current_user=user)

    return _reaction


IMG_COLORS = ('red', 'green', 'blue')


def gen_images():
    """Генерация изображений для тестов"""
    images = []
    for color in IMG_COLORS:
        io = BytesIO()
        img = Image.new(mode='RGB', size=(200, 200), color=color)
        img.save(io, format='PNG')
        images.append(('attachments', (f'{color}.png', io, 'image/png')))
    return images


# тестовые данные для тестов
DATASET = {
    'users': {'admin': UserIn(username='Admin', name='Одмен', email='admin@mail.ru', password='admin_password'),
              'user': UserIn(username='User', name='Юзверь', email='user@mail.ru', password='user_password')},
    'posts': {
        'with_attachments': {'text': 'Post with attachments',
                             'attachments': gen_images()},
        'without_attachments': {'text': 'Post without attachments', 'attachments': []}
    }
}
