import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8001"

def test_endpoint(name, method, path, json_data=None, files=None):
    url = f"{BASE_URL}{path}"
    print(f"Testing {name} ({method} {path})...")
    try:
        if method == "GET":
            r = requests.get(url)
        elif method == "POST":
            r = requests.post(url, json=json_data, files=files)
        
        print(f"  Status Code: {r.status_code}")
        try:
            print(f"  Response: {json.dumps(r.json(), indent=2)}")
        except Exception:
            print(f"  Response Raw (Length {len(r.content)}): {r.content[:200]}")
        return r.status_code == 200
    except Exception as e:
        print(f"  ERROR calling endpoint: {e}")
        return False

if __name__ == "__main__":
    print("=== API ENDPOINT TESTS ===")
    
    # 1. Root
    test_endpoint("Root Endpoint", "GET", "/")
    
    # 2. Session Start
    session_ok = test_endpoint("Session Start", "POST", "/session/start")
    
    # 3. Chat
    chat_payload = {
        "messages": [
            {"role": "user", "content": "I have chest pain and shortness of breath."}
        ]
    }
    test_endpoint("Chat Endpoint", "POST", "/chat", json_data=chat_payload)
    
    # 4. Report Generate
    report_payload = {
        "symptoms": "chest pain, shortness of breath",
        "severity_score": 6.5,
        "care_level": "URGENT",
        "recommendation": "Rest and monitor condition."
    }
    test_endpoint("Report Generate", "POST", "/report/generate", json_data=report_payload)

    # 5. Vitals Analyze
    import os
    with open("mock_video.mp4", "wb") as f:
        f.write(b"mock video bytes")
    try:
        with open("mock_video.mp4", "rb") as f:
            test_endpoint("Vitals Analyze", "POST", "/vitals/analyze", files={"file": f})
    finally:
        if os.path.exists("mock_video.mp4"):
            os.remove("mock_video.mp4")

    # 6. Voice Analyze
    with open("mock_audio.wav", "wb") as f:
        f.write(b"mock audio bytes")
    try:
        with open("mock_audio.wav", "rb") as f:
            test_endpoint("Voice Analyze", "POST", "/voice/analyze", files={"file": f})
    finally:
        if os.path.exists("mock_audio.wav"):
            os.remove("mock_audio.wav")

    print("=== TESTS COMPLETE ===")
