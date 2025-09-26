from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "test endpoint works"}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "healthy", "model_loaded": False}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Cats vs Dogs Classifier - Simple Test</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .upload-form { margin: 20px 0; padding: 20px; border: 1px solid #ccc; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🐱🐶 Cats vs Dogs Classifier - Simple Test</h1>
                    <p>Serveur HTTP simple pour tester la fonctionnalité.</p>

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
                        </ul>
                    </div>
                </div>

                <script>
                document.getElementById('predictForm').addEventListener('submit', async function(e) {
                    e.preventDefault();

                    const resultDiv = document.getElementById('result');
                    resultDiv.innerHTML = 'Traitement en cours...';

                    try {
                        // Simulation d'une prédiction sans upload réel
                        const mockResponse = {
                            "filename": "test_image.jpg",
                            "prediction": "Dog",
                            "confidence": "87.3%",
                            "probabilities": {
                                "cat": "12.7%",
                                "dog": "87.3%"
                            },
                            "note": "Réponse simulée - test réussi!"
                        };

                        // Simuler un délai de traitement
                        setTimeout(() => {
                            resultDiv.innerHTML = `<pre>${JSON.stringify(mockResponse, null, 2)}</pre>`;
                        }, 1000);

                    } catch (error) {
                        resultDiv.innerHTML = `<p style="color: red;">Erreur: ${error.message}</p>`;
                        console.error('Erreur:', error);
                    }
                });
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/api/predict':
            # Simple response for prediction
            response = {
                "filename": "uploaded_image.jpg",
                "prediction": "Dog",
                "confidence": "87.3%",
                "probabilities": {
                    "cat": "12.7%",
                    "dog": "87.3%"
                },
                "note": "Réponse de test - serveur HTTP simple"
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8001), SimpleHandler)
    print("🚀 Serveur de test démarré sur http://localhost:8001")
    print("📱 Ouvrez votre navigateur et allez sur http://localhost:8001")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    server.serve_forever()