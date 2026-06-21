import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.database import Base
from app.models.user import User

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

    session.execute(text("DELETE FROM users"))
    session.commit()
    session.close()