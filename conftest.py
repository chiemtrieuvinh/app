import pytest
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import get_database_url


# Set ALL required environment variables before any imports
os.environ["DB_ENGINE"] = "postgresql"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_USERNAME"] = "test"
os.environ["DB_PASSWORD"] = "test"
os.environ["DB_NAME"] = "test.db"
os.environ["DB_PORT"] = "5432"
os.environ["DEFAULT_PASSWORD"] = "test_password"
os.environ["JWT_SECRET_KEY"] = "test_secret_key"
os.environ["JWT_ALGORITHM"] = "HS256"

from database import get_db_context
from schemas.base import Base
from main import app

SQLALCHEMY_DATABASE_URL = get_database_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    app.dependency_overrides[get_db_context] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def mock_env_vars():
    pass 