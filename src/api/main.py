import sys
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Ajouter les chemins nécessaires
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.settings import API_CONFIG
from src.models.predictor import CatDogPredictor

app = FastAPI(title="Cats vs Dogs Classifier", version="1.0.0")
security = HTTPBearer()

# Initialisation du prédicteur
predictor = CatDogPredictor()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_CONFIG["token"]:
        raise HTTPException(status_code=401, detail="Token invalide")
    return credentials.credentials

@app.get("/")
async def root():
    return {
        "message": "Cats vs Dogs Classifier API",
        "version": "1.0.0",
        "model_loaded": predictor.is_loaded(),
        "endpoints": {
            "info": "/info",
            "predict": "/api/predict (POST, token requis)",
            "docs": "/docs"
        }
    }

@app.get("/info")
async def info():
    return {
        "model_name": "Cats vs Dogs Classifier",
        "version": "1.0.0",
        "model_loaded": predictor.is_loaded(),
        "classes": ["Cat", "Dog"],
        "input_size": f"{predictor.image_size[0]}x{predictor.image_size[1]}",
        "parameters": predictor.model.count_params() if predictor.is_loaded() else 0
    }

@app.post("/api/predict")
async def predict(file: UploadFile = File(...), token: str = Depends(verify_token)):
    if not predictor.is_loaded():
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image")
    
    try:
        image_data = await file.read()
        result = predictor.predict(image_data)
        
        return {
            "filename": file.filename,
            "prediction": result["prediction"],
            "confidence": f"{result['confidence']:.2%}",
            "probabilities": {
                "cat": f"{result['probabilities']['cat']:.2%}",
                "dog": f"{result['probabilities']['dog']:.2%}"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": predictor.is_loaded()
    }