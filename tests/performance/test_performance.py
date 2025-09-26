#!/usr/bin/env python3
"""Tests de performance de l'application"""

import pytest
import time
import asyncio
import aiohttp
import psutil
import numpy as np
from pathlib import Path
import sys

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.api.main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_response_time(client):
    """Test du temps de réponse de l'API"""
    start_time = time.time()
    response = client.get("/api/monitoring")
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 1.0  # La réponse doit être < 1 seconde

@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test des requêtes simultanées"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(10):  # Test avec 10 requêtes simultanées
            task = session.get("http://localhost:8000/api/monitoring")
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        # Vérifier que toutes les requêtes ont réussi
        assert all(r.status == 200 for r in responses)

def test_memory_usage(client):
    """Test de l'utilisation mémoire"""
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # En MB
    
    # Faire plusieurs requêtes
    for _ in range(100):
        response = client.get("/api/monitoring")
        assert response.status_code == 200
    
    final_memory = process.memory_info().rss / 1024 / 1024
    
    # Vérifier qu'il n'y a pas de fuite mémoire importante
    assert (final_memory - initial_memory) < 50  # Moins de 50MB d'augmentation

def test_database_performance():
    """Test des performances de la base de données"""
    from database.models import get_recent_predictions
    
    start_time = time.time()
    predictions = get_recent_predictions(limit=1000)
    query_time = time.time() - start_time
    
    assert query_time < 1.0  # La requête doit être < 1 seconde
    
def test_chart_rendering_speed(client):
    """Test de la vitesse de rendu des graphiques"""
    start_time = time.time()
    response = client.get("/api/monitoring")
    data = response.json()
    
    # Simuler le traitement côté client des données pour les graphiques
    predictions = data["inference"]["predictions"]
    time_series = data["inference"]["time_series"]
    
    processing_time = time.time() - start_time
    
    assert processing_time < 0.5  # Le traitement doit être < 0.5 seconde
    assert isinstance(predictions, dict)
    assert isinstance(time_series, list)