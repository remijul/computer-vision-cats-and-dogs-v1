import requests
import sys
from pathlib import Path

# Test de l'API de prédiction
def test_predict_api():
    """Test the predict API"""
    try:
        print("🔍 Testing predict API...")

        # Test health endpoint first
        url = "http://localhost:8000/health"
        print(f"📡 Calling: {url}")

        response = requests.get(url, timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Content-Type: {response.headers.get('content-type', 'unknown')}")
        print(f"📄 Response: {response.text[:200]}")

        # Test info endpoint
        url = "http://localhost:8000/api/info"
        print(f"\n📡 Calling: {url}")

        response = requests.get(url, timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Content-Type: {response.headers.get('content-type', 'unknown')}")

        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ JSON parsing successful")
                print(f"📈 Response: {data}")
                return True
            except Exception as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"📄 Raw response: {response.text[:500]}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"📄 Response: {response.text[:500]}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_predict_api()