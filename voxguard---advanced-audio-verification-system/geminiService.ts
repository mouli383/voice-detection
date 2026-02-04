
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
    const API_URL = "https://voice-detection-f5x9.onrender.com/api/voice-detection";
    const API_KEY = "sk_test_123456789"; // Configuration for the backend

    try {
      console.log("📡 Sending request to Voice Detection Backend...");

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": API_KEY
        },
        body: JSON.stringify({
          // Defaulting to English if not specified, or we could add language selection to UI
          // For now, ensuring the API contract is met.
          language: "English",
          audioFormat: "mp3",
          audioBase64: audioBase64
        })
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      return result as DetectionResponse;

    } catch (error) {
      console.error("Forensic analysis failure:", error);
      return {
        status: "error",
        message: "The sensitive forensic engine encountered a connection error. Please verify the backend is live."
      } as any; // Cast to bypass strict type if needed, or better, match type
    }
  }
}

export const voiceService = new VoiceDetectionService();
