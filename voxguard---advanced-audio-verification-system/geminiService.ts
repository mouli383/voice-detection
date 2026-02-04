
import { GoogleGenAI, Type } from "@google/genai";
import { DetectionResponse } from "./types";

export class VoiceDetectionService {
  private engine: GoogleGenAI;

  constructor() {
    this.engine = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });
  }

  async analyzeVoice(
    audioBase64: string
  ): Promise<DetectionResponse> {
    try {
      // Upgrading to Pro for deeper forensic reasoning capabilities
      const response = await this.engine.models.generateContent({
        model: "gemini-3-pro-preview",
        contents: [
          {
            parts: [
              {
                inlineData: {
                  mimeType: "audio/mp3",
                  data: audioBase64,
                },
              },
              {
                text: `You are an advanced forensic acoustic engineer. Your objective is to perform a high-fidelity audit of the provided audio to distinguish between organic human speech and synthetic (AI) generation.

AUTHENTICATION PROTOCOL:
1. IDENTIFY LANGUAGE: Determine if the sample is Tamil, English, Hindi, Malayalam, or Telugu.
2. SPECTRAL AUDIT: Analyze for "Phase Locking" or "Harmonic Ghosting" typical of neural vocoders.
3. TEMPORAL ANALYSIS: Check for micro-timing irregularities. AI speech often has unnatural rhythmic precision even when simulating "naturalness."
4. PROOF OF LIFE (POL) MARKERS: Scrutinize for involuntary human artifacts:
   - Natural aspiration (breathing patterns correlated with phrasing).
   - Dental/Labial clicks (moisture sounds in the mouth).
   - Involuntary vocal fold tremors or organic fatigue.
   - Background environment "bleed" or room-tone variance.

CLASSIFICATION RULES:
- Classify as 'HUMAN' if you detect POL markers or irregular spectral noise consistent with organic physiology.
- Classify as 'AI_GENERATED' if the speech shows hyper-consistent pitch modulation, a flat "digital" noise floor, or lack of micro-prosodic emotional resonance.

IMPORTANT: Do not be fooled by high audio quality. Focus on the underlying physical authenticity of the vocal source.

Return exactly this JSON structure:
{
  "status": "success",
  "language": "Identified Language",
  "classification": "AI_GENERATED" | "HUMAN",
  "confidenceScore": float (0.0 - 1.0),
  "explanation": "Detailed technical justification focusing on the presence or absence of organic artifacts."
}`,
              },
            ],
          },
        ],
        config: {
          thinkingConfig: { thinkingBudget: 4000 },
          responseMimeType: "application/json",
          responseSchema: {
            type: Type.OBJECT,
            properties: {
              status: { type: Type.STRING },
              language: { type: Type.STRING },
              classification: { type: Type.STRING },
              confidenceScore: { type: Type.NUMBER },
              explanation: { type: Type.STRING },
            },
            required: ["status", "language", "classification", "confidenceScore", "explanation"],
          },
        },
      });

      const result = JSON.parse(response.text);
      return result as DetectionResponse;
    } catch (error) {
      console.error("Forensic analysis failure:", error);
      return {
        status: "error",
        message: "The forensic engine encountered a spectral processing error."
      };
    }
  }
}

export const voiceService = new VoiceDetectionService();
