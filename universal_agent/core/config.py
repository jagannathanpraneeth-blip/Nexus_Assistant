import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Core
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Database
    DB_PATH = os.getenv("DB_PATH", "universal_agent.db")
    
    # LLM Provider
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")  # mock, openai, gemini
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-in-prod")

    @classmethod
    def validate(cls):
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            print("WARNING: LLM_PROVIDER is openai but OPENAI_API_KEY is missing.")
        if cls.LLM_PROVIDER == "gemini" and not cls.GOOGLE_API_KEY:
            print("WARNING: LLM_PROVIDER is gemini but GOOGLE_API_KEY is missing.")
