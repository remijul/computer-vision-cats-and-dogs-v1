from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form
from datetime import datetime
import sys
from pathlib import Path
import time

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from .auth import verify_token
from src.models.predictor import CatDogPredictor
from src.monitoring.metrics import time_inference
from src.utils.database import get_db_connection

# Configuration des templates
TEMPLATES_DIR = ROOT_DIR / "src" / "web" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()

# Initialisation du prédicteur
predictor = CatDogPredictor()

@router.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    """Page d'accueil avec interface web"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "model_loaded": predictor.is_loaded()
    })

@router.get("/info", response_class=HTMLResponse)
async def info_page(request: Request):
    """Page d'informations"""
    model_info = {
        "name": "Cats vs Dogs Classifier",
        "version": "1.0.0",
        "description": "Modèle CNN pour classification chats/chiens",
        "parameters": predictor.model.count_params() if predictor.is_loaded() else 0,
        "classes": ["Cat", "Dog"],
        "input_size": f"{predictor.image_size[0]}x{predictor.image_size[1]}",
        "model_loaded": predictor.is_loaded()
    }
    return templates.TemplateResponse("info.html", {
        "request": request, 
        "model_info": model_info
    })

@router.get("/inference", response_class=HTMLResponse)
async def inference_page(request: Request):
    """Page d'inférence"""
    return templates.TemplateResponse("inference.html", {
        "request": request,
        "model_loaded": predictor.is_loaded()
    })

@router.post("/api/predict")
@time_inference  # Décorateur de monitoring
async def predict_api(
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    """API de prédiction avec monitoring"""
    if not predictor.is_loaded():
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Format d'image invalide")
    image_data = await file.read()
    result = predictor.predict(image_data)
    response_data = {
        "filename": file.filename,
        "prediction": result["prediction"],
        "confidence": f"{result['confidence']:.2%}",
        "probabilities": {
            "cat": f"{result['probabilities']['cat']:.2%}",
            "dog": f"{result['probabilities']['dog']:.2%}"
        }
    }
    return response_data

@router.post("/api/feedback")
async def submit_feedback(
    log_id: int = Form(...),
    feedback: bool = Form(...),
    predict_result: str = Form(...),
    input_image: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    """
    Soumettre un feedback utilisateur pour l'ajouter à la base de données
    
    Args:
        log_id (int): L'ID du log d'inférence associé.
        feedback (bool): Le feedback utilisateur.
        predict_result (str): Le résultat de la prédiction associée.
        input_image (UploadFile): L'image d'entrée associée.
        
    Returns:
        dict: Un message de confirmation.
    """
    try:
        timestamp = datetime.now().isoformat()
        image_bytes = await input_image.read()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO feedbacks (log_id, feedback, timestamp, predict_result, input_image) 
                VALUES (%s, %s, %s, %s, %s)
            ''', (log_id, feedback, timestamp, predict_result, image_bytes))
            conn.commit()
        return {"detail": "Feedback soumis avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur interne : {str(e)}")
    

@router.get("/api/info")
async def api_info():
    """Informations API JSON"""
    return {
        "model_loaded": predictor.is_loaded(),
        "model_path": str(predictor.model_path),
        "version": "1.0.0",
        "parameters": predictor.model.count_params() if predictor.is_loaded() else 0
    }

@router.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "model_loaded": predictor.is_loaded()
    }