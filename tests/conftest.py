import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient

from app.main import app
from app.database import get_database

client = MongoClient()
db = client['test_database']


@pytest.fixture(scope='module')
def mock_db():
    # set up the mock database
    yield db
    client.drop_database('test_database')


@pytest.fixture(scope='module')
def test_client():
    def _get_test_database():
        return db

    app.dependency_overrides[get_database] = _get_test_database
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}
