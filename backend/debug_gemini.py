import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def test_text():
    print("Testing Text Generation...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content("Hello, can you hear me?")
        print(f"✅ Text Success: {response.text[:50]}...")
    except Exception as e:
        print(f"❌ Text Failed: {e}")

def test_audio():
    print("\nTesting Audio Generation...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Programmatic Valid Base64 (1 frame mp3 header roughly)
    import base64
    mp3_data = b'\xFF\xE3\x18\xC4\x00\x00\x00\x03\x48\x00\x00\x00\x00'
    audio_bytes = mp3_data
    
    try:
        # Try explicit Part construction if implicit fails
        print("Sending audio bytes...")
        response = model.generate_content([
            "Describe this audio",
            {
                "mime_type": "audio/mp3",
                "data": audio_bytes
            }
        ])
        print(f"✅ Audio Success: {response.text[:50]}...")
    except Exception as e:
        print(f"❌ Audio Failed: {e}")

if __name__ == "__main__":
    if not api_key:
        print("No API Key found!")
    else:
        test_text()
        test_audio()
