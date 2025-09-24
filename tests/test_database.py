#!/usr/bin/env python3
"""Tests unitaires des fonctions liées à la base de données (database.py, metrics.py, API directe)"""
import pytest
import sys
from pathlib import Path
import asyncio

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.utils.database import get_db_connection
from src.monitoring.metrics import log_inference_time
from src.api.routes import submit_feedback
from tests.test_api import find_test_image
from config.settings import DATA_DIR
from psycopg2.extensions import connection as Connection

@pytest.fixture(scope="function")
def db_conn():
    """
    Fixture Pytest pour fournir une connexion à la base de données de test.
    - Ouvre une connexion et une transaction avant chaque test.
    - Annule (rollback) la transaction après chaque test pour nettoyer.
    """
    conn = None
    try:
        conn = get_db_connection()
        yield conn
    finally:
        if conn:
            conn.rollback() # Annule toutes les modifications faites pendant le test
            conn.close()

def test_get_db_connection(db_conn: Connection):
    """Teste si la connexion à la base de données est bien une connexion psycopg2."""
    assert db_conn is not None
    assert not db_conn.closed
    # Vérifie que les tables existent (créées par get_db_connection)
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT to_regclass('public.logs');")
        assert cursor.fetchone()[0] == 'logs'
        cursor.execute("SELECT to_regclass('public.feedbacks');")
        assert cursor.fetchone()[0] == 'feedbacks'

def test_log_inference_time_adds_log(db_conn: Connection):
    """Teste si log_inference_time ajoute bien une ligne dans la table 'logs'."""
    log_id = log_inference_time(inference_time_ms=42.0, success=True)
    assert isinstance(log_id, int)

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT inference_time_ms, success FROM logs WHERE id = %s", (log_id,))
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == 42.0
        assert row[1] is True

@pytest.mark.asyncio
async def test_submit_feedback_direct(db_conn: Connection):
    """Teste l'ajout d'un feedback en appelant directement la fonction de la route."""
    # Insérer un log parent pour respecter la contrainte de clé étrangère
    with db_conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO logs (inference_time_ms, success) VALUES (%s, %s) RETURNING id",
            (99.99, True)
        )
        log_id = cursor.fetchone()[0]
        db_conn.commit()

    img_path = find_test_image()

    class DummyUploadFile:
        """Classe factice pour simuler un UploadFile de FastAPI."""
        def __init__(self, path):
            self.filename = path.name
            self._path = path
        async def read(self):
            return self._path.read_bytes()

    result = await submit_feedback(
        log_id=log_id,
        feedback=True,
        predict_result="Cat",
        input_image=DummyUploadFile(img_path),
        token="FAKE_TOKEN" # Le token n'est pas vérifié dans cet appel direct
    )
    assert "Feedback soumis" in result["detail"]

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT predict_result, feedback FROM feedbacks WHERE log_id = %s", (log_id,))
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == "Cat"
        assert row[1] is True
