from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

app = FastAPI(
    title="Cats vs Dogs Classifier - Minimal",
    description="Version minimale pour tests",
    version="1.0.0"
)

# Route de test simple
@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": False}

@app.get("/test")
def test_endpoint():
    return {"message": "test endpoint works"}

@app.post("/api/predict")
def predict_api():
    """API de prédiction simplifiée"""
    return {
        "filename": "test.jpg",
        "prediction": "test_prediction",
        "confidence": "50.0%",
        "probabilities": {
            "cat": "50.0%",
            "dog": "50.0%"
        },
        "note": "Version de test minimale"
    }

# Optionnel : servir des fichiers statiques
STATIC_DIR = ROOT_DIR / "src" / "web" / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")