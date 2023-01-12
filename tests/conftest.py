import pytest

from typing import Generator, Any

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings
from core.utils.attachments import get_attachment_path
from db.crud.posts_cruds import create_new_post
from db.crud.reactions_cruds import create_reaction
from db.crud.users_crud import create_new_user
from db.database import Base, get_db
from db.models import User, Post
from routes import auth_routes, posts_routes, attachments_routes, users_routes, reactions_routes
from schemas.reactions_schemas import ReactionData, get_reaction_entity_id_column, ReactionTypes
from tests.dataset.db_test_dataset import DATASET


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


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """Создаём новую БД для каждого теста"""
    Base.metadata.create_all(engine)
    _app = start_app()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    """Использование сессии в тестах"""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)

    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(
        app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """Клиент для тестирования"""

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    def _get_attachment_path():
        return settings.POST_TEST_ATTACHMENTS_PATH

    # перегрузка зависимостей
    app.dependency_overrides[get_db] = _get_test_db
    app.dependency_overrides[get_attachment_path] = _get_attachment_path
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def user_admin(db_session):
    return create_new_user(user=DATASET['users']['admin'], db=db_session)


@pytest.fixture(scope="module")
def user_common(db_session):
    return create_new_user(user=DATASET['users']['user'], db=db_session)


@pytest.fixture(scope="module")
def post_with_attachments(db_session, user: User):
    post = DATASET['posts']['post_with_attachments']
    return create_new_post(text=post['text'], attachments=post['attachments'], current_user=user, db=db_session)


@pytest.fixture(scope="module")
def post_without_attachments(db_session, user: User):
    post = DATASET['posts']['post_without_attachments']
    return create_new_post(text=post['text'], attachments=post['attachments'], current_user=user, db=db_session)


@pytest.fixture(scope="module")
def reaction(db_session, user: User, entity: Base, reaction_type: str):
    reaction_data = ReactionData(entity_id_column=get_reaction_entity_id_column(clsname=entity.__class__.__name__),
                                 entity=entity,
                                 reaction_type=ReactionTypes[reaction_type].value, reaction_db=None)
    return create_reaction(reaction_data=reaction_data, db=db_session, current_user=user)
