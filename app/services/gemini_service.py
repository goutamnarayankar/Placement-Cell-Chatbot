import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

from app.services.nlp_service import nlp_bot  # NLP fallback if Gemini fails

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("🔑 GEMINI_API_KEY Loaded?", bool(GEMINI_API_KEY))

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing in environment/.env")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# From your list_models.py output
MODEL_ID = "models/gemini-2.5-flash"

# ========================================================
#   SYSTEM PROMPT – SHORT, DIRECT, PLACEMENT-FOCUSED
# ========================================================

SYSTEM_PROMPT = """
You are PlacementAI — a friendly, practical placement mentor for Indian engineering students.

STYLE:
- Reply in simple English.
- 3–6 lines maximum.
- Use bullet points only when useful.
- Never write long essays.
- Be direct, clear and encouraging.

CONTEXT HANDLING:
- Remember details from earlier in the conversation: skills, CGPA, branch, year, projects, interests.
- DO NOT keep asking the same questions again and again.
- If the user has already given CGPA, skills, branch, year, or projects, use them directly.

PLACEMENT LOGIC:
- If user asks things like:
  * "show me companies"
  * "companies I'm eligible for"
  * "which jobs can I get"
  then you MUST:
  1) Infer their eligibility from given CGPA, skills, branch, projects.
  2) Suggest 4–8 example companies (mix of service + product/startups) like:
     - TCS, Infosys, Wipro, Cognizant, Capgemini, Accenture
     - For stronger skills: Amazon, Microsoft, Google, Flipkart, Zoho, startups.
  3) Briefly explain WHY they fit (CGPA OK / skills match / good for freshers).
  4) Give 1–2 next steps (DSA, projects, resume, mock interviews).

- If user has no experience but has projects:
  * Treat projects as experience.
  * Give beginner-friendly roles and companies.

- If user is stressed, anxious or says "I'm scared", "I'm stressed":
  * First 1–2 lines: emotional support, normalizing their feeling.
  * Then: 2–3 concrete, simple steps they can start with.

RESUME:
- If resume context is provided, use it to:
  * Mention key skills, projects and strengths.
  * Suggest job roles and companies aligned with that resume.

ABSOLUTE RULES:
- Never reply with only more questions when the user clearly asked for "companies" or "jobs".
- Even if information is incomplete, make reasonable assumptions and still give:
  * job roles
  * example companies
  * a short action plan.
"""


# ========================================================
#  UNIVERSAL CHAT – GEMINI + NLP FALLBACK
# ========================================================

async def gemini_chat(user_message: str, history: str = "", resume_context: str = "") -> str:
    """
    Smart chat:
    - Uses full conversation history so Gemini remembers CGPA, skills, projects, etc.
    - Uses SYSTEM_PROMPT to force company suggestions when asked.
    - Falls back to simple NLP if Gemini fails.
    """

    full_prompt = f"""
{SYSTEM_PROMPT}

Conversation so far:
{history}

Resume context (if any):
{resume_context}

New user message:
{user_message}

As PlacementAI, respond now.
"""

    try:
        model = genai.GenerativeModel(MODEL_ID)
        resp = model.generate_content(full_prompt)
        text = (resp.text or "").strip()

        if text:
            return text

        # If Gemini returns empty, fallback to NLP
        return nlp_bot.reply(user_message)

    except Exception as e:
        print("⚠️ Gemini chat error:", e)
        return nlp_bot.reply(user_message)


# ========================================================
#  RESUME ANALYSIS – RETURNS STRUCTURED DATA
# ========================================================

async def analyze_resume(resume_text: str) -> dict:
    """
    Ask Gemini to return JSON ONLY with score, summary, skills, roles, weaknesses and recommendations.
    """

    prompt = f"""
You are an AI resume evaluator and placement mentor.

Analyze this resume text and return ONLY valid JSON (no commentary):

Resume:
\"\"\"{resume_text}\"\"\"

JSON format:
{{
  "score": 0-100,
  "summary": "1-2 line summary of the candidate",
  "skills_detected": ["skill1", "skill2"],
  "job_roles": ["role1", "role2"],
  "weaknesses": ["weakpoint1", "weakpoint2"],
  "recommendations": ["rec1", "rec2"]
}}
"""

    try:
        model = genai.GenerativeModel(MODEL_ID)
        resp = model.generate_content(prompt)
        raw = (resp.text or "").strip()
        cleaned = raw.replace("```json", "").replace("```", "")
        data = json.loads(cleaned)
        return data

    except Exception as e:
        print("⚠️ Resume analyze error:", e)
        return {
            "score": 0,
            "summary": "Resume analysis failed.",
            "skills_detected": [],
            "job_roles": [],
            "weaknesses": [str(e)],
            "recommendations": []
        }
