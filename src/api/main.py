from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Importer les routes
try:
    from .routes import router
    print("✅ Import routes réussi")
except Exception as e:
    print(f"❌ Erreur import routes: {e}")
    import traceback
    traceback.print_exc()
    router = None

from database import init_database

app = FastAPI(
    title="Cats vs Dogs Classifier",
    description="API de classification d'images chats vs chiens avec interface web",
    version="1.0.0"
)

# Gestionnaire d'erreurs global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": {
                "error": "Erreur interne du serveur",
                "message": str(exc),
                "type": exc.__class__.__name__,
                "status": 500
            }
        }
    )

# Route de santé
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": False}
    return {"message": "test endpoint works"}

# @app.get("/")
# async def home():
#     return {"message": "Cats vs Dogs Classifier API"}

# Initialisation de la base de données au démarrage
init_database()

# Ajouter les routes
try:
    if router is not None:
        app.include_router(router)
        print("✅ Routes incluses avec succès")
    else:
        print("⚠️ Router is None, skipping inclusion")
except Exception as e:
    print(f"❌ Erreur lors de l'inclusion des routes: {e}")
    import traceback
    traceback.print_exc()

# Optionnel : servir des fichiers statiques
STATIC_DIR = ROOT_DIR / "src" / "web" / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")