import requests

try:
    response = requests.get('http://localhost:8001/test')
    print('Test endpoint:', response.text)
except Exception as e:
    print('Erreur:', e)