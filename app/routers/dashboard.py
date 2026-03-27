from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.core.db import get_current_user, db
import json

router = APIRouter()

@router.get("/dashboard")
async def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/auth/login")

    rows = db().execute("""
        SELECT id, summary, strengths, improvements, missing_skills, roles, resume_score, created_at
        FROM resume_analysis
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user["id"],)).fetchall()

    history = []
    for r in rows:
        history.append({
            "id": r["id"],
            "summary": r["summary"],
            "strengths": json.loads(r["strengths"]) if r["strengths"] else [],
            "improvements": json.loads(r["improvements"]) if r["improvements"] else [],
            "missing_skills": json.loads(r["missing_skills"]) if r["missing_skills"] else [],
            "roles": json.loads(r["roles"]) if r["roles"] else [],
            "score": r["resume_score"],
            "created_at": r["created_at"]
        })

    return request.app.templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "history": history})
