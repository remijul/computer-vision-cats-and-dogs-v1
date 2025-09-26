import requests

# Test simple
try:
    response = requests.post('http://localhost:8000/api/predict',
                           headers={'Authorization': 'Bearer ?C@TS&D0GS!'})
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Response: {response.text[:200]}...")
except Exception as e:
    print(f"Error: {e}")