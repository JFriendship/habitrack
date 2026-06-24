import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.database import Base
from app.models.user import User
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

@pytest.fixture()
def db_session():
    session = TestSessionLocal()

    yield session

    session.execute(text("DELETE FROM habits"))
    session.execute(text("DELETE FROM users"))
    session.commit()
    session.close()


@pytest.fixture()
def test_user(db_session):
    return register_user(
        db=db_session,
        user_create=UserCreate(
            username="test_user", email="testuser@gmail.com", password="testuser"
        )
    )
