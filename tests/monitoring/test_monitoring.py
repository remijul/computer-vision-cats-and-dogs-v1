#!/usr/bin/env python3
"""Tests pytest du système de monitoring"""

import pytest
from pathlib import Path
import sys
import time
from datetime import datetime
import csv
import tempfile
import os

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.monitoring.metrics import log_inference_time, ensure_monitoring_file
from config.settings import PROCESSED_DATA_DIR

@pytest.fixture
def temp_monitoring_file():
    """Crée un fichier de monitoring temporaire"""
    temp_dir = tempfile.mkdtemp()
    temp_file = Path(temp_dir) / "test_monitoring.csv"
    
    original_file = PROCESSED_DATA_DIR / "monitoring_inference.csv"
    original_path = str(original_file)
    
    # Remplacer temporairement le fichier de monitoring
    os.environ["MONITORING_FILE"] = str(temp_file)
    
    yield temp_file
    
    # Restaurer le fichier original
    os.environ["MONITORING_FILE"] = original_path
    
    # Nettoyer
    if temp_file.exists():
        temp_file.unlink()
    os.rmdir(temp_dir)

def test_log_inference_time(temp_monitoring_file):
    """Test l'enregistrement du temps d'inférence"""
    inference_time = 150.5  # 150.5ms
    log_inference_time(inference_time, success=True)
    
    assert temp_monitoring_file.exists()
    
    with open(temp_monitoring_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        row = rows[0]
        assert float(row['inference_time_ms']) == pytest.approx(150.5)
        assert row['success'] == 'True'
        # Vérifier que la date est valide
        datetime.fromisoformat(row['timestamp'])

def test_log_inference_multiple_entries(temp_monitoring_file):
    """Test l'enregistrement de plusieurs temps d'inférence"""
    times = [100.0, 150.0, 200.0]
    for t in times:
        log_inference_time(t, success=True)
    
    with open(temp_monitoring_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        # +1 pour le header
        assert len(rows) == len(times) + 1

def test_log_inference_failure(temp_monitoring_file):
    """Test l'enregistrement d'une inférence échouée"""
    log_inference_time(100.0, success=False)
    
    with open(temp_monitoring_file, 'r') as f:
        reader = csv.DictReader(f)
        row = next(reader)
        assert row['success'] == 'False'

def test_ensure_monitoring_file(temp_monitoring_file):
    """Test la création du fichier de monitoring"""
    # Supprimer le fichier s'il existe
    if temp_monitoring_file.exists():
        temp_monitoring_file.unlink()
    
    ensure_monitoring_file()
    
    assert temp_monitoring_file.exists()
    with open(temp_monitoring_file, 'r') as f:
        header = f.readline().strip().split(',')
        assert 'timestamp' in header
        assert 'inference_time_ms' in header
        assert 'success' in header