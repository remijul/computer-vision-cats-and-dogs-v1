import csv
import logging
import time
from datetime import datetime
from pathlib import Path
from functools import wraps
import sys

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import ROOT_DIR, PROCESSED_DATA_DIR
from src.utils.database import get_db_connection
from fastapi import HTTPException
 
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
            VALUES (%s, %s, %s) RETURNING id
        ''', (timestamp, inference_time_ms, success))
        conn.commit()
        # Récupère l'ID retourné par la requête
        log_id = cursor.fetchone()[0]
    return log_id

def log_user_feedback(log_id: int, feedback: bool, predict_result: str, input_image_bytes: bytes):
    """
    Logger le feedback utilisateur dans la base de données.

    Args:
        log_id (int): L'ID du log d'inférence associé.
        feedback (bool): Le feedback utilisateur (True pour correct, False pour incorrect).
        predict_result (str): Le résultat de la prédiction.
        input_image_bytes (bytes): L'image d'entrée en bytes.
    
    Raises:
        ValueError: Si le log_id n'existe pas.
    """
    timestamp = datetime.now().isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Vérifier que le log_id existe
        cursor.execute("SELECT id FROM logs WHERE id = %s", (log_id,))
        if cursor.fetchone() is None:
            raise ValueError(f"Le log avec l'ID {log_id} n'existe pas.")

        cursor.execute('''
            INSERT INTO feedbacks (log_id, feedback, timestamp, predict_result, input_image) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (log_id, feedback, timestamp, predict_result, input_image_bytes))
        conn.commit()




def time_inference(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        logging.debug(f"Starting inference timing for {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            success = True
        except HTTPException as e:
            # Log quand même l'échec, puis relance l'exception pour FastAPI
            end_time = time.perf_counter()
            inference_time_ms = (end_time - start_time) * 1000
            log_inference_time(inference_time_ms=inference_time_ms, success=False)
            raise
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