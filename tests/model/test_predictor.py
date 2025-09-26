import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from src.models.predictor import CatDogPredictor
import io

# Tester le predictor directement
print('Test du predictor...')
try:
    predictor = CatDogPredictor()
    print(f'Modèle chargé: {predictor.is_loaded()}')

    # Tester avec des données fake
    fake_data = io.BytesIO(b'fake image data')
    result = predictor.predict(fake_data)
    print(f'Résultat: {result}')
except Exception as e:
    print(f'Erreur: {e}')
    import traceback
    traceback.print_exc()