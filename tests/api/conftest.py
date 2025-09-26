"""Fixtures partagées pour les tests API."""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

@pytest.fixture
def client():
    """Fixture du client de test FastAPI."""
    return TestClient(app)