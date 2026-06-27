import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db.dependencies import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.main import app
from app.models.user import User
from app.models.habit import Habit
from app.services.user_service import register_user
from app.schemas.user import UserCreate

test_engine = create_engine(settings.TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session():
    session = TestSessionLocal()

    yield session

    session.execute(text("DELETE FROM habit_completions"))
    session.execute(text("DELETE FROM habits"))
    session.execute(text("DELETE FROM users"))
    session.commit()
    session.close()


@pytest.fixture
def test_user(db_session):
    return register_user(
        db=db_session,
        user_create=UserCreate(
            username="test_user", email="testuser@gmail.com", password="testuser"
        )
    )


@pytest.fixture
def created_habit(db_session, test_user: User):
    habit = Habit(name="Exercise", description="30 minutes daily", user_id=test_user.id)

    db_session.add(habit)
    db_session.commit()
    db_session.refresh(habit)

    return habit

@pytest.fixture
def auth_headers(test_user: User):
    access_token = create_access_token(str(test_user.id))

    return {
        "Authorization": f"Bearer {access_token}"
    }

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()