import requests
import os
import json

# Minimal test script without unicode characters
def check_api():
    url = "https://voice-detection-f5x9.onrender.com/api/voice-detection"
    print(f"Checking {url}...")
    
    # Valid MP3 Base64 (short silence)
    b64 = "//NExAAAAANIAAAAAExBTUUzLjEwMKqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//NExAAAAANIAAAAAExBTUUzLjEwMKqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
    
    payload = {
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": b64
    }
    
    headers = {
        "x-api-key": "sk_test_123456789",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        print(f"Status: {r.status_code}")
        print("Response Body:")
        print(r.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_api()
