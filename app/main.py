import os
from dotenv import load_dotenv

# Load .env BEFORE anything else
load_dotenv()
print("🔑 Loaded GEMINI_API_KEY?", bool(os.getenv("GEMINI_API_KEY")))

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Core DB + Session Utilities
from app.core.db import init_db, get_current_user

# Routers
from app.routers import auth, resume, chat, dashboard, company


# ---------------------------------------------------------
#                FASTAPI APP INITIALIZATION
# ---------------------------------------------------------
app = FastAPI(title="Placement AI Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (CSS / JS / Images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")
app.templates = templates


# ---------------------------------------------------------
#                     DATABASE INIT
# ---------------------------------------------------------
init_db()


# ---------------------------------------------------------
#                   ROOT REDIRECT (LOGIN FIRST)
# ---------------------------------------------------------
@app.get("/")
async def home(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse("/dashboard")
    return RedirectResponse("/auth/login")


# ---------------------------------------------------------
#                   ROUTER REGISTRATION
# ---------------------------------------------------------
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(chat.router)
app.include_router(dashboard.router)
app.include_router(company.router)


# ---------------------------------------------------------
#                     MAIN RUNNER
# ---------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Placement AI Hub is running!")
    print("👉 Visit: http://127.0.0.1:8000\n")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
