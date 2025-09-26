import requests
import json

# Tester les différents endpoints
base_url = 'http://localhost:8000'

print("=== Test des endpoints ===\n")

# 1. Test health
print("1. Test /health:")
try:
    response = requests.get(f'{base_url}/health')
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"   Response: {response.text}")
    if response.headers.get('Content-Type') == 'application/json':
        try:
            data = response.json()
            print("   ✓ JSON valide")
        except:
            print("   ✗ JSON invalide")
    print()
except Exception as e:
    print(f"   Erreur: {e}\n")

# 2. Test predict sans authentification
print("2. Test /api/predict (sans auth):")
try:
    response = requests.post(f'{base_url}/api/predict')
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"   Response: {response.text[:200]}...")
    if response.headers.get('Content-Type') == 'application/json':
        try:
            data = response.json()
            print("   ✓ JSON valide")
        except:
            print("   ✗ JSON invalide")
    print()
except Exception as e:
    print(f"   Erreur: {e}\n")

# 3. Test predict avec authentification mais sans fichier
print("3. Test /api/predict (avec auth, sans fichier):")
try:
    headers = {'Authorization': 'Bearer ?C@TS&D0GS!'}
    response = requests.post(f'{base_url}/api/predict', headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"   Response: {response.text[:200]}...")
    if response.headers.get('Content-Type') == 'application/json':
        try:
            data = response.json()
            print("   ✓ JSON valide")
        except:
            print("   ✗ JSON invalide")
    print()
except Exception as e:
    print(f"   Erreur: {e}\n")

# 4. Test predict avec auth et fichier simulé
print("4. Test /api/predict (avec auth et fichier simulé):")
try:
    headers = {'Authorization': 'Bearer ?C@TS&D0GS!'}
    # Créer un fichier temporaire simulé
    import io
    fake_image = io.BytesIO(b"fake image data")
    fake_image.name = 'test.jpg'
    files = {'file': ('test.jpg', fake_image, 'image/jpeg')}

    response = requests.post(f'{base_url}/api/predict', headers=headers, files=files)
    print(f"   Status: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"   Response: {response.text[:500]}...")
    if response.headers.get('Content-Type') == 'application/json':
        try:
            data = response.json()
            print("   ✓ JSON valide")
        except json.JSONDecodeError as je:
            print(f"   ✗ JSON invalide: {je}")
            print(f"   Premier caractère: '{response.text[0] if response.text else 'vide'}'")
    else:
        print(f"   ✗ Pas du JSON - Content-Type: {response.headers.get('Content-Type')}")
    print()
except Exception as e:
    print(f"   Erreur: {e}\n")