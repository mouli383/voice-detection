import requests
import json
import base64
import os

# Create a dummy mp3 file content (header only roughly) or just random bytes that look enough like a file for transmission test
# Better: minimal valid mp3 frame
mp3_data = b'\xFF\xE3\x18\xC4\x00\x00\x00\x03\x48\x00\x00\x00\x00' # Dummy frame
full_mp3_b64 = base64.b64encode(mp3_data).decode('utf-8')

def test_full_integration():
    print("🚀 Starting End-to-End Integration Test...")
    
    url = "http://localhost:8000/api/voice-detection"
    headers = {
        "x-api-key": "sk_test_123456789",
        "Content-Type": "application/json"
    }
    
    # We use a very short dummy audio. Gemini might say "Audio too short" or "Unknown", 
    # but valid JSON response means backend <-> Gemini connection is working.
    payload = {
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": full_mp3_b64
    }
    
    print("\n📡 Sending Request to Local Backend...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS! Backend & Gemini Working Perfectly.")
            print("-" * 40)
            print(json.dumps(data, indent=2))
            print("-" * 40)
        else:
            print(f"❌ Error Response: {response.text}")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_full_integration()
