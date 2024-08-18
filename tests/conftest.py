from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker
import pytest
from fastapi.testclient import TestClient

from app.core.db.database import Base, get_db
from app.core.assistant import Assistant
from app.internal.chats.openai_assistant import get_assistant
from app.main import app as base_app


SQLITE_DB_URL = "sqlite:///./test.db"


engine = create_engine(
    SQLITE_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestingSession = sessionmaker(autoflush=True, bind=engine)
Base.metadata.create_all(bind=engine)


class TestAssistant(Assistant):
    def get_response_for_prompt(self, prompt: str) -> str:
        assert isinstance(prompt, str)
        return "response from ai"


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSession(bind=engine)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def assistant():
    yield TestAssistant()


@pytest.fixture(scope="function")
def test_client(db_session: Session, assistant: Assistant):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_db_session():
        try:
            yield db_session
        finally:
            db_session.close()

    def override_assistant():
        try:
            yield assistant
        finally:
            pass

    base_app.dependency_overrides[get_db] = override_db_session
    base_app.dependency_overrides[get_assistant] = override_assistant

    with TestClient(base_app) as test_client:
        yield test_client
