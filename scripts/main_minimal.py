from fastapi import FastAPI
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Test import database
try:
    from database import init_database
    print("Database import successful")
    init_database()
    print("Database init successful")
except Exception as e:
    print(f"Database error: {e}")

# Test import routes
try:
    from src.api.routes import router
    print("Routes import successful")
    app.include_router(router)
    print("Routes included")
except Exception as e:
    print(f"Routes error: {e}")
    import traceback
    traceback.print_exc()

# Test predictor initialization
try:
    from src.models.predictor import CatDogPredictor
    predictor = CatDogPredictor()
    print(f"Predictor loaded: {predictor.is_loaded()}")
except Exception as e:
    print(f"Predictor error: {e}")
    import traceback
    traceback.print_exc()

@app.get("/test")
async def test():
    return {"message": "test"}