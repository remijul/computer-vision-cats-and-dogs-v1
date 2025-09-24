#!/usr/bin/env python3
"""Tests unitaires des fonctions liées à la base de données (database.py, metrics.py, API directe)"""
import pytest
from pathlib import Path
from src.utils.database import get_db_connection
from src.monitoring.metrics import log_inference_time
import sqlite3

DB_PATH = Path("data/database.db")

# Test de la fonction utilitaire get_db_connection
def test_get_db_connection_creates_and_opens():
    conn = get_db_connection()
    assert isinstance(conn, sqlite3.Connection)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs';")
    assert cursor.fetchone() is not None
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedbacks';")
    assert cursor.fetchone() is not None
    conn.close()

# Test de log_inference_time (metrics.py)
def test_log_inference_time_adds_log():
    conn = get_db_connection()
    log_id = log_inference_time(42.0, True)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs WHERE id = ?", (log_id,))
    row = cursor.fetchone()
    assert row is not None
    conn.close()

# Test d'ajout de feedback via la fonction API (directe, sans HTTP)
def test_submit_feedback_direct():
    from src.api.routes import submit_feedback
    import asyncio
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, inference_time_ms, success)
        VALUES (datetime('now'), 99.99, 1)
    """)
    conn.commit()
    log_id = cursor.lastrowid
    conn.close()
    img_path = Path("data/raw/PetImages/Cat/6653.jpg")
    if not img_path.exists():
        pytest.skip("Image de test non trouvée")
    class DummyUploadFile:
        def __init__(self, path):
            self.filename = path.name
            self._path = path
        async def read(self):
            with open(self._path, "rb") as f:
                return f.read()
    # Appelle la fonction API directement
    result = asyncio.run(submit_feedback(
        log_id=log_id,
        feedback=True,
        predict_result="Cat",
        input_image=DummyUploadFile(img_path),
        token="FAKE_TOKEN"
    ))
    assert "Feedback soumis" in result["detail"]
    # Vérifie en base
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedbacks WHERE log_id = ?", (log_id,))
    row = cursor.fetchone()
    assert row is not None
    conn.close()
