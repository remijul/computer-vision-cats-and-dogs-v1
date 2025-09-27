import csv
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from functools import wraps
from collections import defaultdict
import sys
from typing import Dict, List, Any

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import ROOT_DIR, PROCESSED_DATA_DIR

# Fichiers CSV pour stocker les métriques
MONITORING_FILE = PROCESSED_DATA_DIR / "monitoring_inference.csv"
FEEDBACK_METRICS_FILE = PROCESSED_DATA_DIR / "monitoring_feedback.csv"

def ensure_monitoring_file():
    """Créer le fichier CSV avec les headers si nécessaire"""
    if not MONITORING_FILE.exists():
        with open(MONITORING_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'inference_time_ms',
                'success',
                'prediction',
                'confidence',
                'file_size_bytes',
                'user_agent'
            ])

def ensure_feedback_metrics_file():
    """Créer le fichier CSV des métriques feedback si nécessaire"""
    if not FEEDBACK_METRICS_FILE.exists():
        with open(FEEDBACK_METRICS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'feedback_value',
                'prediction_result',
                'user_input',
                'response_time_ms'
            ])

def get_db_connection():
    """Retourne une connexion à la base de données SQLite"""
    import sqlite3
    db_path = str(ROOT_DIR / "feedbacks.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Pour avoir des résultats sous forme de dictionnaires
    return conn

def ensure_monitoring_table():
    """S'assurer que la table monitoring_metrics existe"""
    import sqlite3
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Vérifier si la table existe déjà
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='monitoring_metrics'")
    if cursor.fetchone() is None:
        print("Création de la table monitoring_metrics...")
        # Créer la table si elle n'existe pas
        cursor.execute('''
        CREATE TABLE monitoring_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inference_time_ms FLOAT NOT NULL,
            success BOOLEAN NOT NULL,
            prediction TEXT,
            confidence FLOAT,
            file_size_bytes INTEGER,
            user_agent TEXT,
            error TEXT,
            timestamp DATETIME NOT NULL
        )
        ''')
        
        # Créer les index pour optimiser les requêtes
        cursor.execute('CREATE INDEX idx_metrics_timestamp ON monitoring_metrics(timestamp)')
        cursor.execute('CREATE INDEX idx_metrics_success ON monitoring_metrics(success)')
        
        print("Table monitoring_metrics créée avec succès!")
    
    conn.commit()
    conn.close()

def log_inference_time(inference_time_ms: float, success: bool = True, prediction: str = None,
                      confidence: float = None, file_size_bytes: int = None, user_agent: str = None, error: str = None):
    """Enregistrer une métrique d'inférence dans le CSV et dans la base de données SQLite"""
    ensure_monitoring_file()
    ensure_monitoring_table()  # S'assurer que la table SQL existe

    timestamp = datetime.now().isoformat()

    # Enregistrement dans le fichier CSV
    with open(MONITORING_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            round(inference_time_ms, 2),
            success,
            prediction or '',
            round(confidence, 4) if confidence else '',
            file_size_bytes or '',
            user_agent or ''
        ])
    
    # Enregistrement dans la base de données SQLite
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO monitoring_metrics 
            (inference_time_ms, success, prediction, confidence, file_size_bytes, user_agent, error, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            round(inference_time_ms, 2),
            success,
            prediction,
            confidence,
            file_size_bytes,
            user_agent,
            error,
            timestamp
        ))
        
        conn.commit()
        conn.close()
        print(f"✅ Métrique d'inférence enregistrée dans la base de données: {timestamp}, {inference_time_ms}ms")
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement des métriques dans la base de données: {e}")

def log_feedback_metrics(feedback_value: str, prediction_result: str, user_input: str,
                        response_time_ms: float = None):
    """Enregistrer une métrique de feedback"""
    ensure_feedback_metrics_file()

    timestamp = datetime.now().isoformat()

    with open(FEEDBACK_METRICS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            feedback_value,
            prediction_result,
            user_input,
            round(response_time_ms, 2) if response_time_ms else ''
        ])

def get_inference_metrics(hours: int = 24) -> Dict[str, Any]:
    """Récupérer les métriques d'inférence des dernières heures"""
    if not MONITORING_FILE.exists():
        return {"error": "Aucune donnée de monitoring disponible"}

    cutoff_time = datetime.now() - timedelta(hours=hours)
    metrics = {
        "total_requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "avg_inference_time": 0,
        "min_inference_time": float('inf'),
        "max_inference_time": 0,
        "predictions": defaultdict(int),
        "time_series": [],
        "recent_requests": []
    }

    inference_times = []

    with open(MONITORING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                timestamp = datetime.fromisoformat(row['timestamp'])
                if timestamp < cutoff_time:
                    continue

                metrics["total_requests"] += 1
                inference_time = float(row['inference_time_ms'])
                inference_times.append(inference_time)

                if str(row['success']).lower() in ['true', '1', 'yes']:
                    metrics["successful_requests"] += 1
                else:
                    metrics["failed_requests"] += 1

                if inference_time < metrics["min_inference_time"]:
                    metrics["min_inference_time"] = inference_time
                if inference_time > metrics["max_inference_time"]:
                    metrics["max_inference_time"] = inference_time

                if row.get('prediction'):
                    metrics["predictions"][row['prediction']] += 1

                # Données pour le graphique (dernières 50 requêtes)
                if len(metrics["time_series"]) < 50:
                    metrics["time_series"].append({
                        "timestamp": timestamp.isoformat(),
                        "inference_time": inference_time,
                        "success": str(row.get('success', 'true')).lower() == 'true'
                    })

                # Requêtes récentes (dernières 10)
                if len(metrics["recent_requests"]) < 10:
                    metrics["recent_requests"].append({
                        "timestamp": timestamp.isoformat(),
                        "inference_time": inference_time,
                        "prediction": row.get('prediction', ''),
                        "success": str(row.get('success', 'true')).lower() == 'true'
                    })

            except (ValueError, KeyError):
                continue

    if inference_times:
        metrics["avg_inference_time"] = round(sum(inference_times) / len(inference_times), 2)

    if metrics["min_inference_time"] == float('inf'):
        metrics["min_inference_time"] = 0

    return metrics

def get_feedback_metrics(hours: int = 24) -> Dict[str, Any]:
    """Récupérer les métriques de feedback des dernières heures"""
    if not FEEDBACK_METRICS_FILE.exists():
        return {"error": "Aucune donnée de feedback disponible"}

    cutoff_time = datetime.now() - timedelta(hours=hours)
    metrics = {
        "total_feedbacks": 0,
        "positive_feedbacks": 0,
        "negative_feedbacks": 0,
        "accuracy_rate": 0,
        "feedbacks_by_prediction": defaultdict(lambda: {"positive": 0, "negative": 0}),
        "recent_feedbacks": []
    }

    with open(FEEDBACK_METRICS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                timestamp = datetime.fromisoformat(row['timestamp'])
                if timestamp < cutoff_time:
                    continue

                metrics["total_feedbacks"] += 1
                feedback_value = row['feedback_value'].lower()
                prediction = row['prediction_result']

                if feedback_value in ['oui', '1', 'true', 'correct']:
                    metrics["positive_feedbacks"] += 1
                    metrics["feedbacks_by_prediction"][prediction]["positive"] += 1
                else:
                    metrics["negative_feedbacks"] += 1
                    metrics["feedbacks_by_prediction"][prediction]["negative"] += 1

                # Feedbacks récents (dernières 10)
                if len(metrics["recent_feedbacks"]) < 10:
                    metrics["recent_feedbacks"].append({
                        "timestamp": timestamp.isoformat(),
                        "feedback_value": feedback_value,
                        "prediction": prediction,
                        "user_input": row['user_input']
                    })

            except (ValueError, KeyError):
                continue

    if metrics["total_feedbacks"] > 0:
        metrics["accuracy_rate"] = round((metrics["positive_feedbacks"] / metrics["total_feedbacks"]) * 100, 2)

    return metrics

def get_combined_metrics(hours: int = 24) -> Dict[str, Any]:
    """Récupérer toutes les métriques combinées"""
    inference_metrics = get_inference_metrics(hours)
    feedback_metrics = get_feedback_metrics(hours)

    # Convertir defaultdict en dict pour la sérialisation JSON
    if 'predictions' in inference_metrics and isinstance(inference_metrics['predictions'], defaultdict):
        inference_metrics['predictions'] = dict(inference_metrics['predictions'])

    if 'feedbacks_by_prediction' in feedback_metrics and isinstance(feedback_metrics['feedbacks_by_prediction'], defaultdict):
        feedback_metrics['feedbacks_by_prediction'] = dict(feedback_metrics['feedbacks_by_prediction'])

    return {
        "inference": inference_metrics,
        "feedback": feedback_metrics,
        "timestamp": datetime.now().isoformat(),
        "period_hours": hours
    }