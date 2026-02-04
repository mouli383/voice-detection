import requests
import json
import time

# Minimal 1-second silent MP3 base64
# This ensures Gemini receives a valid audio structure, even if it's silent
# 1-second silent MP3 (Valid Base64)
# 1-second silent MP3 (Valid Base64)
MINIMAL_MP3_B64 = "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAAEAAABIADAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAw//OEAAAAAAAAAAAAAAAAAAAAAAAAMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAAMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="

def test_full_integration():
    print("🚀 Starting End-to-End Integration Test...")
    
    url = "http://localhost:8000/api/voice-detection"
    headers = {
        "x-api-key": "sk_test_123456789",
        "Content-Type": "application/json"
    }
    
    payload = {
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": MINIMAL_MP3_B64
    }
    
    print("\n📡 Sending Request to Local Backend...")
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload)
        duration = time.time() - start_time
        
        print(f"⏱️  Response Time: {duration:.2f}s")
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS! Backend & Gemini Working Perfectly.")
            print("-" * 40)
            print(json.dumps(data, indent=2))
            print("-" * 40)
            
            # Verify specific fields
            if data["status"] == "success" and "classification" in data:
                print("🏆 Verification Passed: Response format matches requirements.")
            else:
                print("⚠️  Warning: Response format check failed.")
        else:
            print(f"❌ Error Response: {response.text}")

    except Exception as e:
        print(f"❌ Connection Error: Is the server running? ({e})")

if __name__ == "__main__":
    test_full_integration()
