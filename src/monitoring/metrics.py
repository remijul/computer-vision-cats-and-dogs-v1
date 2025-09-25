import time
from functools import wraps
from src.database.crud import insert_monitoring

def log_inference_time(inference_time_ms: float, success: bool = True):
    """Enregistrer une métrique d'inférence dans la base de données."""
    # Convertir le temps en secondes (optionnel, selon ton besoin)
    inference_time_sec = inference_time_ms / 1000.0
    # Insérer directement dans la base de données
    insert_monitoring(
        time=inference_time_sec,
        succes=success
    )

def time_inference(func):
    """Décorateur pour mesurer le temps d'inférence et logger en base de données."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        try:
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()

            # Calculer le temps en millisecondes
            inference_time_ms = (end_time - start_time) * 1000

            # Logger le succès
            log_inference_time(
                inference_time_ms=inference_time_ms,
                success=True
            )

            return result

        except Exception as e:
            end_time = time.perf_counter()
            inference_time_ms = (end_time - start_time) * 1000

            # Logger l'échec
            log_inference_time(
                inference_time_ms=inference_time_ms,
                success=False
            )

            raise e

    return wrapper