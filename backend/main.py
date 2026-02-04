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

@app.post("/api/voice-detection", response_model=VoiceAnalysisResponse)
async def detect_voice_origin(request: VoiceAnalysisRequest, api_key: str = Depends(verify_api_key)):
    try:
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        # Forensic Inversion Strategy
        prompt_text = f"""
        ACT AS: Senior Forensic Audio Analyst.
        TASK: Determine if vocal source is BIO-ORGANIC (Human) or SYNTHETIC (AI).
        LANGUAGE: {request.language}
        
        FORENSIC CHECKLIST:
        1. SEARCH FOR 'PROOF OF LIFE' (POL):
           - Breathing patterns.
           - Mouth/Lip clicks.
           - Natural Room-tone bleed.
        2. SEARCH FOR 'SYNTHETIC MARKERS' (SM):
           - Robotic spectral consistency.
           - Digital flatness.
        
        DECISION: If POL exists (even if audio is clear), it is HUMAN. If POL is absent and spectral noise is hyper-consistent, it is AI_GENERATED.
        
        Return exactly this JSON:
        {{
            "status": "success",
            "language": "{request.language}",
            "classification": "HUMAN" or "AI_GENERATED",
            "confidenceScore": float,
            "explanation": "Reasoning based on POL/SM markers."
        }}
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt_text}, {"inline_data": {"mime_type": "audio/mp3", "data": request.audioBase64}}]}],
            "safetySettings": [{"category": c, "threshold": "BLOCK_NONE"} for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]],
            "generationConfig": {"temperature": 0.0, "response_mime_type": "application/json"}
        }
        
        response = requests.post(api_url, json=payload, timeout=45)
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")
            
        result = response.json()
        raw_text = result['candidates'][0]['content']['parts'][0]['text']
        result_json = json.loads(raw_text)
        
        return VoiceAnalysisResponse(
            status="success",
            language=request.language,
            classification=result_json.get("classification", "AI_GENERATED"),
            confidenceScore=result_json.get("confidenceScore", 0.0),
            explanation=result_json.get("explanation", "Verification completed.")
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail={"status": "error", "message": str(e)})

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
