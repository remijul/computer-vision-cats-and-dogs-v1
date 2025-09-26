"""Fixtures partagées pour les tests de base de données."""
import pytest
import tempfile
import os
from pathlib import Path
from database.models import create_tables

@pytest.fixture
def test_db():
    """Fixture de base de données de test."""
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    create_tables()
    yield db_path
    if db_path.exists():
        db_path.unlink()
    os.rmdir(temp_dir)