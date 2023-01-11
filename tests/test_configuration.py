import pytest

from typing import Generator, Any

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings
from db.database import Base, get_db
from routes import auth_routes, posts_routes, attachments_routes, users_routes, reactions_routes


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
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """Клиент для тестирования"""
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    # перегрузка get_db зависимости на тестовую сессию
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
