from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import json, pathlib

router = APIRouter()

@router.get("/companies")
async def list_companies():
    path = pathlib.Path(__file__).resolve().parents[1] / "data" / "companies.json"
    companies = json.loads(path.read_text())
    html = "".join(
        f"<div class='company-card'><h3>{c['company']}</h3>"
        f"<p><b>CGPA:</b> {c['cgpa']}</p>"
        f"<p><b>Skills:</b> {', '.join(c['skills'])}</p></div>"
        for c in companies
    )
    return HTMLResponse(html)
