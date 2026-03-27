from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from app.core.db import db, get_current_user
from app.services.pdf_service import extract_text_from_pdf
from app.services.gemini_service import analyze_resume
import json

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(request: Request, file: UploadFile = File(...)):
    user = get_current_user(request)
    if not user:
        return HTMLResponse("Not logged in", status_code=401)

    if file.content_type != "application/pdf":
        return HTMLResponse("Only PDF allowed", status_code=400)

    raw = await file.read()
    text = extract_text_from_pdf(raw)
    analysis = await analyze_resume(text)

    conn = db()
    conn.execute("""
        INSERT INTO resume_analysis (user_id, summary, strengths, improvements, missing_skills, roles, resume_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user["id"],
        analysis.get("summary", ""),
        json.dumps(analysis.get("strengths", [])),
        json.dumps(analysis.get("improvements", [])),
        json.dumps(analysis.get("missing_skills", [])),
        json.dumps(analysis.get("roles", [])),
        int(analysis.get("resume_score", 0))
    ))
    conn.commit()

    return HTMLResponse("OK")
