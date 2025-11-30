from core.config import Config
from cognitive.llm_interface import OpenAIProvider, GeminiProvider
import os

def verify():
    print("--- Configuration Verification ---")
    print(f"ENV: {Config.ENV}")
    print(f"LLM_PROVIDER: {Config.LLM_PROVIDER}")
    
    openai_key = Config.OPENAI_API_KEY
    google_key = Config.GOOGLE_API_KEY
    
    print(f"OpenAI Key: {'[PRESENT]' if openai_key else '[MISSING]'}")
    print(f"Google Key: {'[PRESENT]' if google_key else '[MISSING]'}")
    
    if openai_key:
        try:
            OpenAIProvider()
            print("✅ OpenAI Provider initialized successfully.")
        except Exception as e:
            print(f"❌ OpenAI Provider failed: {e}")

    if google_key:
        try:
            GeminiProvider()
            print("✅ Gemini Provider initialized successfully.")
        except Exception as e:
            print(f"❌ Gemini Provider failed: {e}")

if __name__ == "__main__":
    verify()
