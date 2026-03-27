import secrets
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.db import create_student, verify_password, get_student, SESSIONS

router = APIRouter()


@router.get("/auth/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return request.app.templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/auth/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = get_student(email)
    if not user or not verify_password(password, user["salt"], user["password_hash"]):
        return request.app.templates.TemplateResponse(
            "auth/login.html", {"request": request, "error": "Invalid credentials"}
        )

    token = secrets.token_hex(16)
    SESSIONS[token] = email

    resp = RedirectResponse("/dashboard", status_code=302)
    resp.set_cookie("session", token, httponly=True, samesite="lax", max_age=86400)
    return resp


@router.get("/auth/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return request.app.templates.TemplateResponse("auth/signup.html", {"request": request})


@router.post("/auth/signup")
async def signup(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        create_student(name, email, password)
        return RedirectResponse("/auth/login", status_code=302)
    except Exception:
        return request.app.templates.TemplateResponse(
            "auth/signup.html", {"request": request, "error": "User already exists!"}
        )


@router.get("/auth/logout")
async def logout():
    resp = RedirectResponse("/auth/login", status_code=302)
    resp.delete_cookie("session")
    return resp
