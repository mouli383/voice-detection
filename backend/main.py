from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
import uvicorn
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import base64
import requests
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

app = FastAPI(title="Voice Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def verify_api_key(x_api_key: str = Header(...)):
    valid_key = os.getenv("CALLGUARD_AI_API_KEY", "sk_test_123456789")
    if x_api_key != valid_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

class VoiceAnalysisRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

class VoiceAnalysisResponse(BaseModel):
    status: str
    language: str
    classification: str
    confidenceScore: float
    explanation: str

class ErrorResponse(BaseModel):
    status: str
    message: str

# --- Core Logic ---
@app.post("/api/voice-detection", response_model=VoiceAnalysisResponse)
async def detect_voice_origin(request: VoiceAnalysisRequest, api_key: str = Depends(verify_api_key)):
    # BRUTE FORCE RELIABILITY LIST
    # We will try every single known model alias until one works.
    candidates = [
        "gemini-flash-latest",   # Matches 'models/gemini-flash-latest' from API
        "gemini-pro-latest",     # Matches 'models/gemini-pro-latest' from API
        "gemini-2.0-flash",
        "gemini-1.5-flash", 
        "gemini-1.5-flash-001",
        "gemini-1.5-pro",
        "gemini-1.5-pro-001",
        "gemini-1.0-pro",
        "gemini-pro"
    ]
    
    last_error = None
    success_model = None

    # Forensic Inversion Strategy (The Secret Sauce)
    prompt_text = f"""
    You are an advanced forensic acoustic engineer. Your objective is to perform a high-fidelity audit of the provided audio to distinguish between organic human speech and synthetic (AI) generation.
    
    AUTHENTICATION PROTOCOL:
    IDENTIFY LANGUAGE: Determine if the sample is Tamil, English, Hindi, Malayalam, or Telugu ({request.language} suggested).
    SPECTRAL AUDIT: Analyze for 'Phase Locking' or 'Harmonic Ghosting' typical of neural vocoders.
    TEMPORAL ANALYSIS: Check for micro-timing irregularities. AI speech often has unnatural rhythmic precision even when simulating 'naturalness.'
    
    PROOF OF LIFE (POL) MARKERS: Scrutinize for involuntary human artifacts:
    - Natural aspiration (breathing patterns correlated with phrasing).
    - Dental/Labial clicks (moisture sounds in the mouth).
    - Involuntary vocal fold tremors or organic fatigue.
    - Background environment 'bleed' or room-tone variance.
    
    CLASSIFICATION RULES:
    - Classify as 'HUMAN' if you detect POL markers or irregular spectral noise consistent with organic physiology.
    - Classify as 'AI_GENERATED' if the speech shows hyper-consistent pitch modulation, a flat 'digital' noise floor, or lack of micro-prosodic emotional resonance.
    
    IMPORTANT: Do not be fooled by high audio quality. Focus on the underlying physical authenticity of the vocal source.
    
    Return exactly this JSON structure:
    {{
        "status": "success",
        "language": "{request.language}",
        "classification": "AI_GENERATED" | "HUMAN",
        "confidenceScore": float (0.0 - 1.0),
        "explanation": "Detailed technical justification focusing on the presence or absence of organic artifacts."
    }}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt_text}, {"inline_data": {"mime_type": "audio/mp3", "data": request.audioBase64}}]}],
        "safetySettings": [{"category": c, "threshold": "BLOCK_NONE"} for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 8192, "response_mime_type": "application/json"}
    }

    for model in candidates:
        try:
            print(f"👉 Trying model: {model}...")
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            
            response = requests.post(api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ SUCCESS with {model}!")
                success_model = model
                
                result = response.json()
                raw_text = result['candidates'][0]['content']['parts'][0]['text']
                result_json = json.loads(raw_text)
                
                return VoiceAnalysisResponse(
                    status="success",
                    language=result_json.get("language", request.language),
                    classification=result_json.get("classification", "AI_GENERATED"),
                    confidenceScore=result_json.get("confidenceScore", 0.0),
                    explanation=result_json.get("explanation", f"Verified by Forensic Engine ({model}).")
                )
            
            # If 404 (Not Found) or 403 (Forbidden), just log and continue
            print(f"⚠️ {model} failed with {response.status_code}: {response.text}")
            last_error = f"{model}: {response.status_code}"
            continue

        except Exception as e:
            print(f"❌ {model} exception: {e}")
            last_error = f"{model} Error: {str(e)}"
            continue

    # If we made it here, ALL models failed.
    print(f"🔥 FATAL: All models failed. Last error: {last_error}")
    raise HTTPException(
        status_code=500, 
        detail={"status": "error", "message": f"Service Unavailable. Tried all models. Last error: {last_error}"}
    )

@app.get("/")
def home():
    return {"status": "online", "system": "VoxGuard Neural Forensic Engine", "version": "5.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok", "model_backend": "gemini-1.5-flash-001"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
