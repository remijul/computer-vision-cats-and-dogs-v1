from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sys
from pathlib import Path
import time

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from .auth import verify_token
from src.models.predictor import CatDogPredictor
from src.monitoring.metrics import time_inference, log_inference_time
from src.monitoring.advanced_metrics import log_feedback_metrics, get_combined_metrics
from database import save_feedback

# Configuration des templates
TEMPLATES_DIR = ROOT_DIR / "src" / "web" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()

# Initialisation du prédicteur
predictor = None
try:
    predictor = CatDogPredictor()
    print(f"✅ Prédicteur initialisé: {predictor.is_loaded()}")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation du prédicteur: {e}")
    predictor = None
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sys
from pathlib import Path
import time

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from .auth import verify_token
from src.models.predictor import CatDogPredictor
from src.monitoring.metrics import time_inference, log_inference_time
from src.monitoring.advanced_metrics import log_feedback_metrics, get_combined_metrics
from database import save_feedback

# Configuration des templates
TEMPLATES_DIR = ROOT_DIR / "src" / "web" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()

# Initialisation du prédicteur
predictor = None
try:
    predictor = CatDogPredictor()
    print(f"✅ Prédicteur initialisé: {predictor.is_loaded()}")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation du prédicteur: {e}")
    import traceback
    traceback.print_exc()
    predictor = None

@router.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    """Page d'accueil avec interface web"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "model_loaded": predictor is not None and predictor.is_loaded()
    })

@router.get("/info", response_class=HTMLResponse)
async def info_page(request: Request):
    """Page d'informations"""
    model_info = {
        "name": "Cats vs Dogs Classifier",
        "version": "1.0.0",
        "description": "Modèle CNN pour classification chats/chiens",
        "parameters": predictor.model.count_params() if predictor is not None and predictor.is_loaded() else 0,
        "classes": ["Cat", "Dog"],
        "input_size": f"{predictor.image_size[0]}x{predictor.image_size[1]}" if predictor is not None else "224x224",
        "model_loaded": predictor is not None and predictor.is_loaded()
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
        "model_loaded": predictor is not None and predictor.is_loaded()
    })

@router.post("/api/predict")
async def predict_api(
    request: Request,
    file: UploadFile = File(...),
    # token: str = Depends(verify_token)  # Temporairement désactivé pour debug
):
    """API de prédiction avec monitoring"""
    start_time = time.perf_counter()

    print(f"DÉBUG: Début de la prédiction pour {file.filename}")

    if predictor is None or not predictor.is_loaded():
        print("DÉBUG: Modèle non chargé - réponse d'erreur")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Service non disponible",
                "message": "Le modèle n'est pas chargé actuellement",
                "status": 503
            }
        )

    if not file.content_type.startswith('image/'):
        print(f"DÉBUG: Content-type invalide: {file.content_type}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Format invalide",
                "message": "Le fichier doit être une image (JPG, PNG, etc.)",
                "status": 400
            }
        )
    
    try:
        print("DÉBUG: Lecture du fichier...")
        image_data = await file.read()
        print(f"DÉBUG: Fichier lu, taille: {len(image_data)} bytes")
        
        if not image_data:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Fichier invalide",
                    "message": "Le fichier image est vide",
                    "status": 400
                }
            )
        
        print("DÉBUG: Prédiction en cours...")
        try:
            result = predictor.predict(image_data)
        except Exception as e:
            print(f"DÉBUG: Erreur de prédiction: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Erreur de prédiction",
                    "message": str(e),
                    "status": 500
                }
            )
            
        print(f"DÉBUG: Prédiction terminée: {result}")
        
        # Calculer le temps d'inférence
        end_time = time.perf_counter()
        inference_time_ms = (end_time - start_time) * 1000
        
        response_data = {
            "filename": file.filename,
            "prediction": result["prediction"],
            "confidence": f"{result['confidence']:.2%}",
            "probabilities": {
                "cat": f"{result['probabilities']['cat']:.2%}",
                "dog": f"{result['probabilities']['dog']:.2%}"
            }
        }
        
        print(f"DÉBUG: Réponse préparée: {response_data}")
        
        # Logger les métriques avec tous les détails
        from src.monitoring.advanced_metrics import log_inference_time
        log_inference_time(
            inference_time_ms=inference_time_ms,
            success=True,
            prediction=result["prediction"],
            confidence=result["confidence"],
            file_size_bytes=len(image_data),
            user_agent=request.headers.get("user-agent", "")
        )
        
        return response_data
        
    except Exception as e:
        # En cas d'erreur, logger quand même le temps
        end_time = time.perf_counter()
        inference_time_ms = (end_time - start_time) * 1000
        
        print(f"DÉBUG: Erreur dans la prédiction: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        from src.monitoring.advanced_metrics import log_inference_time
        log_inference_time(
            inference_time_ms=inference_time_ms,
            success=False,
            error=str(e),
            file_size_bytes=len(image_data) if 'image_data' in locals() else 0,
            user_agent=request.headers.get("user-agent", "")
        )
        
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")

@router.get("/api/info")
async def api_info():
    """Informations API JSON"""
    return {
        "model_loaded": predictor is not None and predictor.is_loaded(),
        "model_path": str(predictor.model_path) if predictor is not None else "N/A",
        "version": "1.0.0",
        "parameters": predictor.model.count_params() if predictor is not None and predictor.is_loaded() else 0
    }

@router.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "model_loaded": predictor is not None and predictor.is_loaded()
    }

@router.post("/api/feedback")
async def submit_feedback(
    feedback_data: dict,
    token: str = Depends(verify_token)
):
    """API pour soumettre un feedback utilisateur"""
    try:
        prediction_result = feedback_data.get("prediction_result")
        user_input = feedback_data.get("user_input")
        feedback_value = feedback_data.get("feedback_value")
        
        if not all([prediction_result, user_input, feedback_value]):
            raise HTTPException(status_code=400, detail="Données de feedback incomplètes")
        
        if feedback_value not in ["oui", "non"]:
            raise HTTPException(status_code=400, detail="Valeur de feedback invalide (doit être 'oui' ou 'non')")
        
        # Sauvegarder le feedback dans la base de données
        feedback_id = save_feedback(feedback_value, prediction_result, user_input)

        # Logger les métriques de feedback
        log_feedback_metrics(
            feedback_value=feedback_value,
            prediction_result=prediction_result,
            user_input=user_input
        )
        
        return {
            "success": True,
            "message": "Feedback enregistré avec succès",
            "feedback_id": feedback_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement du feedback: {str(e)}")

@router.get("/monitoring", response_class=HTMLResponse)
async def monitoring_page(request: Request):
    """Page de monitoring des performances du modèle"""
    try:
        metrics = get_combined_metrics(hours=24)

        # Convertir defaultdict en dict pour le template
        if 'predictions' in metrics['inference']:
            metrics['inference']['predictions'] = dict(metrics['inference']['predictions'])
        if 'feedbacks_by_prediction' in metrics['feedback']:
            metrics['feedback']['feedbacks_by_prediction'] = dict(metrics['feedback']['feedbacks_by_prediction'])

        return templates.TemplateResponse("monitoring.html", {
            "request": request,
            "metrics": metrics,
            "model_loaded": predictor is not None and predictor.is_loaded()
        })

    except Exception as e:
        return templates.TemplateResponse("monitoring.html", {
            "request": request,
            "metrics": {"error": str(e)},
            "model_loaded": predictor is not None and predictor.is_loaded()
        })

@router.get("/api/monitoring")
async def get_monitoring_api(hours: int = 24):
    """API pour récupérer les métriques de monitoring"""
    try:
        return get_combined_metrics(hours)
    except Exception as e:
        return {"error": str(e)}