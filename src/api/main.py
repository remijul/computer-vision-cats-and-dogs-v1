from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from .routes import router

app = FastAPI(
    title="Cats vs Dogs Classifier",
    description="API de classification d'images chats vs chiens avec interface web",
    version="1.0.0"
)

# Ajouter les routes
app.include_router(router)

# Optionnel : servir des fichiers statiques
STATIC_DIR = ROOT_DIR / "src" / "web" / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")