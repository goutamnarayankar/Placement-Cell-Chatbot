import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print("🔑 Loaded:", bool(key))

genai.configure(api_key=key)

print("\n📌 AVAILABLE MODELS IN YOUR GEMINI ACCOUNT:\n")
models = genai.list_models()

for m in models:
    print("-", m.name)
