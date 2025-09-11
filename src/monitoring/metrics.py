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

def log_inference_time(inference_time_ms: float, success: bool = True):
    """Enregistrer une métrique d'inférence dans le CSV"""
    ensure_monitoring_file()
    
    timestamp = datetime.now().isoformat()
    
    with open(MONITORING_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            round(inference_time_ms, 2),
            success
        ])

def time_inference(func):
    """Décorateur pour mesurer le temps d'inférence"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        try:
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            
            # Calculer le temps en millisecondes
            inference_time_ms = (end_time - start_time) * 1000
            
            # Extraire les informations du résultat si possible
            if hasattr(result, 'body'):
                # FastAPI Response object
                import json
                try:
                    response_data = json.loads(result.body)
                    log_inference_time(
                        inference_time_ms=inference_time_ms,
                        success=True
                    )
                except:
                    log_inference_time(inference_time_ms, success=True)
            else:
                # Dict response
                log_inference_time(
                    inference_time_ms=inference_time_ms,
                    success=True
                )
            
            return result
            
        except Exception as e:
            end_time = time.perf_counter()
            inference_time_ms = (end_time - start_time) * 1000
            
            # Logger l'erreur
            log_inference_time(
                inference_time_ms=inference_time_ms,
                success=False
            )
            
            raise e
    
    return wrapper