from fastapi.testclient import TestClient
from main import app
import os
from dotenv import load_dotenv

load_dotenv()

client = TestClient(app)

def run_diagnostics():
    print("🔍 Starting Local Backend Diagnostics...")
    
    # 1. Health Check
    try:
        response = client.get("/health")
        if response.status_code == 200 and response.json() == {"status": "ok"}:
            print("✅ Health Check Endpoint: OK")
        else:
            print(f"❌ Health Check Endpoint: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Health Check Error: {e}")

    # 2. Authentication
    try:
        # Valid Key
        valid_key = os.getenv("CALLGUARD_AI_API_KEY", "sk_test_123456789")
        
        # Test Missing Header
        resp_missing = client.post("/api/voice-detection", json={})
        # 422 Unprocessable Entity (missing header)
        if resp_missing.status_code == 422:
             print("✅ Auth System: Correctly rejects missing header")
        else:
             print(f"❌ Auth System: Failed to reject missing header (Got {resp_missing.status_code})")

        # Test Invalid Key
        resp_invalid = client.post("/api/voice-detection", headers={"x-api-key": "invalid_key_123"}, json={})
        if resp_invalid.status_code == 401:
             print("✅ Auth System: Correctly rejects invalid key")
        else:
             print(f"❌ Auth System: Failed to reject invalid key (Got {resp_invalid.status_code})")

    except Exception as e:
        print(f"❌ Auth Test Error: {e}")

    # 3. Request Validation
    try:
        headers = {"x-api-key": valid_key}
        payload = {
            "language": "Tamil",
            # Missing audioFormat and audioBase64
        }
        resp = client.post("/api/voice-detection", headers=headers, json=payload)
        if resp.status_code == 422:
             print("✅ Validation: Correctly requests missing fields")
        else:
             print(f"❌ Validation: Accepted incomplete data (Got {resp.status_code})")

    except Exception as e:
        print(f"❌ Validation Error: {e}")
            
    print("\nℹ️  To test full AI analysis, ensure GEMINI_API_KEY is in .env and run the server.")

if __name__ == "__main__":
    run_diagnostics()
