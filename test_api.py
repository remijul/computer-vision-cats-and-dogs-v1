#!/usr/bin/env python3
"""Test script to diagnose the monitoring API issue"""

import requests
import json

def test_monitoring_api():
    """Test the monitoring API"""
    try:
        print("🔍 Testing monitoring API...")

        # Test the API endpoint
        url = "http://127.0.0.1:8000/api/monitoring?hours=24"
        print(f"📡 Calling: {url}")

        response = requests.get(url, timeout=10)

        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Content-Type: {response.headers.get('content-type', 'unknown')}")

        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ JSON parsing successful")
                print(f"📈 Keys in response: {list(data.keys())}")

                if 'inference' in data:
                    print(f"   - Inference requests: {data['inference']['total_requests']}")
                if 'feedback' in data:
                    print(f"   - Feedbacks: {data['feedback']['total_feedbacks']}")

                return True

            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"📄 Raw response (first 500 chars): {response.text[:500]}")
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
    success = test_monitoring_api()
    if not success:
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure the server is running: python scripts/run_api.py")
        print("2. Check if port 8000 is available")
        print("3. Verify the API route exists in routes.py")