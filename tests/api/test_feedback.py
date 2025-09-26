#!/usr/bin/env python3
"""Tests pytest des fonctionnalités de feedback"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys
import json

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.api.main import app
from config.settings import API_CONFIG

client = TestClient(app)
TOKEN = API_CONFIG["token"]

@pytest.fixture
def auth_headers():
    """Headers d'authentification pour les tests"""
    return {"Authorization": f"Bearer {TOKEN}"}

def test_feedback_endpoint_success(auth_headers):
    """Test l'envoi d'un feedback positif"""
    feedback_data = {
        "prediction_result": "Cat",
        "user_input": "test_image.jpg",
        "feedback_value": "oui"
    }
    
    response = client.post(
        "/api/feedback",
        headers=auth_headers,
        json=feedback_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True

def test_feedback_endpoint_invalid_data(auth_headers):
    """Test l'envoi d'un feedback avec données invalides"""
    feedback_data = {
        "prediction_result": "Invalid",
        "feedback_value": "maybe"
    }
    
    response = client.post(
        "/api/feedback",
        headers=auth_headers,
        json=feedback_data
    )
    
    assert response.status_code == 400

def test_feedback_endpoint_no_auth():
    """Test l'envoi d'un feedback sans authentification"""
    feedback_data = {
        "prediction_result": "Cat",
        "feedback_value": "oui"
    }
    
    response = client.post(
        "/api/feedback",
        json=feedback_data
    )
    
    assert response.status_code == 401

def test_get_feedback_metrics(auth_headers):
    """Test la récupération des métriques de feedback"""
    response = client.get(
        "/api/metrics/feedback",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "total_feedback" in data
    assert "positive_feedback" in data
    assert isinstance(data["total_feedback"], int)
    assert isinstance(data["positive_feedback"], int)