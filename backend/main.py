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
# --- Core Logic ---
@app.post("/api/voice-detection", response_model=VoiceAnalysisResponse)
async def detect_voice_origin(request: VoiceAnalysisRequest, api_key: str = Depends(verify_api_key)):
    # Candidate models from user's availability list
    # We prioritize the "3 Pro Preview" as requested, then 2.0 Flash
    candidates = [
        "gemini-3-pro-preview",
        "gemini-2.0-flash",
        "gemini-2.0-flash-001",
        "gemini-1.5-flash"
    ]

    last_error = None
    genai.configure(api_key=GEMINI_API_KEY)

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

    for model_name in candidates:
        try:
            print(f"👉 SDK Trying model: {model_name}...")
            
            # Configure Generation Config with Thinking Budget if supported (v2/v3 mainly)
            # We map the user's "thinkingBudget: 4000" to "max_output_tokens" for compatibility
            generation_config = {
                "temperature": 0.0,
                "max_output_tokens": 4000, 
                "response_mime_type": "application/json"
            }

            model = genai.GenerativeModel(model_name)
            
            # Construct content part similar to SDK format
            response = model.generate_content(
                contents=[
                    {"role": "user", "parts": [
                        {"text": prompt_text},
                        {"inline_data": {"mime_type": "audio/mp3", "data": request.audioBase64}}
                    ]}
                ],
                generation_config=generation_config,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            # Parse result
            if response.text:
                print(f"✅ SUCCESS with {model_name}!")
                result_json = json.loads(response.text)
                
                return VoiceAnalysisResponse(
                    status="success",
                    language=result_json.get("language", request.language),
                    classification=result_json.get("classification", "AI_GENERATED"),
                    confidenceScore=result_json.get("confidenceScore", 0.0),
                    explanation=result_json.get("explanation", f"Verified by Forensic Engine ({model_name}).")
                )
            else:
                 raise Exception("Empty response from model")

        except Exception as e:
            print(f"❌ {model_name} exception: {e}")
            last_error = f"{model_name} Error: {str(e)}"
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
