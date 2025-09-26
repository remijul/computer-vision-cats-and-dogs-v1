import uvicorn
import sys
import os
from pathlib import Path

# Définir PYTHONPATH explicitement
ROOT_DIR = Path(__file__).parent
os.environ['PYTHONPATH'] = str(ROOT_DIR)
sys.path.insert(0, str(ROOT_DIR))

# Import simple sans décorateurs
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Cats vs Dogs Classifier",
    description="API de classification d'images chats vs chiens avec interface web",
    version="1.0.0"
)

# Route de test simple
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.get("/")
async def home():
    return {"message": "Cats vs Dogs Classifier API"}

if __name__ == "__main__":
    print("Starting simplified server...")
    uvicorn.run(app, host='localhost', port=8000)