import csv
import time
from datetime import datetime
from pathlib import Path
from functools import wraps
import sys

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import ROOT_DIR, PROCESSED_DATA_DIR
from src.utils.database import get_db_connection, close_db_connection
 
# Fichier CSV pour stocker les métriques
MONITORING_FILE = PROCESSED_DATA_DIR / "monitoring_inference.csv"

def ensure_monitoring_file():
    """Créer le fichier CSV avec les headers si nécessaire"""
    if not MONITORING_FILE.exists():
        with open(MONITORING_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'inference_time_ms',
                'success'
            ])

def log_inference_time(inference_time_ms: float, success: bool):
    """
    Logger le temps d'inférence dans la base de données

    Args:
        inference_time_ms (float): Le temps d'inférence en millisecondes.
        success (bool): Indique si l'inférence a réussi ou non.
    """
    timestamp = datetime.now().isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO logs (timestamp, inference_time_ms, success)
            VALUES (?, ?, ?)
        ''', (timestamp, inference_time_ms, success))
        conn.commit()
        # retourne l'id du log inséré
        log_id = cursor.lastrowid
    return log_id

def time_inference(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            success = True
        except Exception as e:
            result = e
            success = False
        end_time = time.perf_counter()
        inference_time_ms = (end_time - start_time) * 1000
        log_id = log_inference_time(inference_time_ms=inference_time_ms, success=success)
        # Toujours renvoyer log_id dans la réponse, même en cas d'erreur
        if isinstance(result, dict):
            result["log_id"] = log_id
            return result
        elif not success:
            # Retourne une réponse d'erreur standardisée avec log_id
            return {"error": str(result), "log_id": log_id}
        return result
    return wrapper