import os
from dotenv import load_dotenv

# ✅ Force load .env from project root
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")

settings = Settings()

print("🔑 Loaded GEMINI_API_KEY?", bool(settings.GEMINI_API_KEY))
