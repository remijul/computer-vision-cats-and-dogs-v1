import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from src.monitoring.advanced_metrics import get_combined_metrics

if __name__ == "__main__":
    try:
        metrics = get_combined_metrics()
        print("Métriques récupérées avec succès:")
        print(metrics)
    except Exception as e:
        print(f"Erreur lors de la récupération des métriques: {e}")
        import traceback
        traceback.print_exc()