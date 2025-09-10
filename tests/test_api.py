import requests
import os

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = "CAT&DOGS!"
IMAGE_PATH = "test_image.jpg"  # Remplacez par votre image de test

def test_api():
    # Test de la page d'accueil
    print("Test page d'accueil...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    
    # Test des infos
    print("\nTest page info...")
    response = requests.get(f"{BASE_URL}/info")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Infos du modèle récupérées")
    
    # Test de prédiction
    if os.path.exists(IMAGE_PATH):
        print(f"\nTest prédiction avec {IMAGE_PATH}...")
        headers = {"Authorization": f"Bearer {TOKEN}"}
        with open(IMAGE_PATH, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/inference", files=files, headers=headers)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Prédiction: {result['prediction']}")
            print(f"Confiance: {result['confidence']}")
    else:
        print(f"\nImage de test {IMAGE_PATH} introuvable")

if __name__ == "__main__":
    test_api()