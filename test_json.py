import sys
import json
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from src.monitoring.advanced_metrics import get_combined_metrics

if __name__ == "__main__":
    try:
        metrics = get_combined_metrics()
        json_str = json.dumps(metrics)
        print("JSON sérialisé avec succès:")
        print(json_str[:500] + "..." if len(json_str) > 500 else json_str)
    except Exception as e:
        print(f"Erreur lors de la sérialisation JSON: {e}")
        import traceback
        traceback.print_exc()