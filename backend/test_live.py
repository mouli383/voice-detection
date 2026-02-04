import requests
import json

# User's Render URL
DEPLOYED_URL = "https://voice-detection-f5x9.onrender.com/api/voice-detection"

# Valid MP3 Base64 (Sine Wave)
VALID_MP3_B64 = """
SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjYwLjEwMAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAABPAABw6AAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQ//OEAAAAAAAAAAAAAAAAAAAAAAAAMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAAMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAAMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAAMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAAMTAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
"""

def test_live():
    if "REPLACE" in DEPLOYED_URL:
        print("❌ Please update the DEPLOYED_URL variable with your Render URL first!")
        return

    print(f"🌍 Connecting to {DEPLOYED_URL}...")
    
    clean_b64 = VALID_MP3_B64.strip().replace("\n", "")
    
    payload = {
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": clean_b64
    }
    
    headers = {
        "x-api-key": "sk_test_123456789",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(DEPLOYED_URL, headers=headers, json=payload, timeout=30)
        
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ LIVE DEPLOYMENT SUCCESS!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Failed. Status: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_live()
