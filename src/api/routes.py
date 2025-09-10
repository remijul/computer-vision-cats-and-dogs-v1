from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth import verify_token
from ..model.predictor import CatDogPredictor
from config.settings import API_CONFIG
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")

# Initialisation du prédicteur
predictor = CatDogPredictor(API_CONFIG["model_path"])

@router.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    """Page d'accueil avec interface web"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/info", response_class=HTMLResponse)
async def info_page(request: Request):
    """Page d'informations"""
    model_info = {
        "name": "Cats vs Dogs Classifier",
        "version": "1.0.0",
        "description": "Modèle CNN pour classification chats/chiens",
        "parameters": predictor.model.count_params() if predictor.is_loaded() else 0,
        "classes": ["Cat", "Dog"],
        "input_size": f"{API_CONFIG.get('image_size', (128, 128))[0]}x{API_CONFIG.get('image_size', (128, 128))[1]}"
    }
    return templates.TemplateResponse("info.html", {
        "request": request, 
        "model_info": model_info
    })

@router.get("/inference", response_class=HTMLResponse)
async def inference_page(request: Request):
    """Page d'inférence"""
    return templates.TemplateResponse("inference.html", {"request": request})

@router.post("/api/predict")
async def predict_api(
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    """API de prédiction"""
    if not predictor.is_loaded():
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Format d'image invalide")
    
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

@router.get("/api/info")
async def api_info():
    """Informations API JSON"""
    return {
        "model_loaded": predictor.is_loaded(),
        "model_path": str(API_CONFIG["model_path"]),
        "version": "1.0.0"
    }