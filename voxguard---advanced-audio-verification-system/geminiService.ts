import { DetectionResponse } from "./types";

export class VoiceDetectionService {
  constructor() { }

  async analyzeVoice(
    audioBase64: string,
    language: string
  ): Promise<DetectionResponse> {
    const API_URL = "https://voice-detection-f5x9.onrender.com/api/voice-detection";
    const API_KEY = "sk_test_123456789";

    try {
      console.log(`📡 Sending request for ${language} audio...`);

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": API_KEY
        },
        body: JSON.stringify({
          language: language,
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
      } as any;
    }
  }
}

export const voiceService = new VoiceDetectionService();
