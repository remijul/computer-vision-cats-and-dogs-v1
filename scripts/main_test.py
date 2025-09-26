from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

app = FastAPI(
    title="Cats vs Dogs Classifier - Test",
    description="Version de test simplifiée",
    version="1.0.0"
)

# Route de santé
@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": False}

# Route de test
@app.get("/test")
def test_endpoint():
    return {"message": "test endpoint works"}

# Page d'accueil simple
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cats vs Dogs Classifier - Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .upload-form { margin: 20px 0; padding: 20px; border: 1px solid #ccc; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐱🐶 Cats vs Dogs Classifier - Test</h1>
            <p>Version de test simplifiée pour diagnostiquer les problèmes.</p>

            <div class="upload-form">
                <h2>Tester la prédiction</h2>
                <form id="predictForm" enctype="multipart/form-data">
                    <input type="file" id="imageInput" accept="image/*" required>
                    <button type="submit">Prédire</button>
                </form>
                <div id="result"></div>
            </div>

            <div>
                <h2>Endpoints de test</h2>
                <ul>
                    <li><a href="/health">/health</a></li>
                    <li><a href="/test">/test</a></li>
                    <li><a href="/api/info">/api/info</a></li>
                </ul>
            </div>
        </div>

        <script>
        document.getElementById('predictForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData();
            const fileInput = document.getElementById('imageInput');
            formData.append('file', fileInput.files[0]);

            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = 'Traitement en cours...';

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                resultDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            } catch (error) {
                resultDiv.innerHTML = `<p style="color: red;">Erreur: ${error.message}</p>`;
                console.error('Erreur:', error);
            }
        });
        </script>
    </body>
    </html>
    """

# API de prédiction simplifiée (sans modèle)
@app.post("/api/predict")
def predict_api(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "prediction": "test_prediction",
        "confidence": "50.0%",
        "probabilities": {
            "cat": "50.0%",
            "dog": "50.0%"
        },
        "note": "Ceci est une réponse de test - modèle non chargé"
    }

# API info
@app.get("/api/info")
def api_info():
    return {
        "model_loaded": False,
        "version": "1.0.0-test",
        "note": "Version de test sans modèle TensorFlow"
    }