"""
Test script to verify all API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_home():
    """Test home endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"[HOME] Status: {response.status_code}")
        print(f"[HOME] Response: {response.text[:100]}")
        return response.status_code == 200
    except Exception as e:
        print(f"[HOME] Error: {e}")
        return False

def test_chat():
    """Test chat endpoint with NLP"""
    try:
        payload = {"message": "I have acne, what should I do?"}
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        print(f"[CHAT] Status: {response.status_code}")
        data = response.json()
        print(f"[CHAT] Response: {data.get('reply', '')[:100]}")
        return response.status_code == 200
    except Exception as e:
        print(f"[CHAT] Error: {e}")
        return False

def test_analyze_form():
    """Test form analysis endpoint"""
    try:
        payload = {
            "skinType": "Oily",
            "ageGroup": "20-30",
            "concerns": ["acne", "oiliness"]
        }
        response = requests.post(f"{BASE_URL}/analyze-form", json=payload)
        print(f"[ANALYZE-FORM] Status: {response.status_code}")
        data = response.json()
        print(f"[ANALYZE-FORM] Skin Type: {data.get('skinType')}")
        print(f"[ANALYZE-FORM] Concerns: {data.get('concerns')}")
        print(f"[ANALYZE-FORM] Recommendations: {len(data.get('recommended_products', []))} products")
        return response.status_code == 200
    except Exception as e:
        print(f"[ANALYZE-FORM] Error: {e}")
        return False

def test_recommend():
    """Test recommend endpoint"""
    try:
        payload = {"concerns": ["acne", "oiliness"]}
        response = requests.post(f"{BASE_URL}/recommend", json=payload)
        print(f"[RECOMMEND] Status: {response.status_code}")
        data = response.json()
        print(f"[RECOMMEND] Recommendations: {len(data.get('recommendations', []))} products")
        return response.status_code == 200
    except Exception as e:
        print(f"[RECOMMEND] Error: {e}")
        return False

def main():
    print("=" * 60)
    print("TESTING ALL API ENDPOINTS")
    print("=" * 60)
    
    # Give server time to start
    print("\nWaiting for server to start...")
    time.sleep(2)
    
    tests = [
        ("Home Endpoint", test_home),
        ("Chat Endpoint (NLP)", test_chat),
        ("Analyze Form Endpoint", test_analyze_form),
        ("Recommend Endpoint", test_recommend),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'-' * 60}")
        print(f"Testing: {test_name}")
        print(f"{'-' * 60}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'=' * 60}")
    print("TEST SUMMARY")
    print(f"{'=' * 60}")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nAll tests passed! The backend is working correctly.")
    else:
        print(f"\n{total - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()
