from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from app.core.db import get_current_user
from app.services.gemini_service import gemini_chat
from app.services.translate_service import Translator

router = APIRouter()

# Simple in-memory chat history per user/session
CHAT_HISTORY = {}   # key: session_id (email or IP), value: list of "User: ..."/"AI: ..." lines

translator = Translator()
LANG = {"current": "en"}


@router.post("/chat/lang")
async def change_lang(lang: str = Form(...)):
    LANG["current"] = lang
    return HTMLResponse(f"<div class='ai-msg'>🌐 Language changed to {lang}</div>")


@router.post("/chat/send")
async def chat_send(request: Request, message: str = Form(...)):
    user = get_current_user(request)

    # Use email as session id if logged in, else fallback to client IP
    session_id = user["email"] if user else (request.client.host or "anonymous")

    # Get previous conversation history
    history_list = CHAT_HISTORY.get(session_id, [])
    history_text = "\n".join(history_list)

    # Language handling – assume translator works
    current_lang = LANG["current"]
    msg_en = await translator.to_en(message, current_lang)

    # TODO: if you store resume summary in DB, fetch it here
    resume_context = ""  # for now nothing

    # Call Gemini with history so it remembers CGPA, skills, projects, etc.
    reply_en = await gemini_chat(msg_en, history=history_text, resume_context=resume_context)

    # Update history (keep last 20 lines)
    history_list.append(f"User: {msg_en}")
    history_list.append(f"AI: {reply_en}")
    CHAT_HISTORY[session_id] = history_list[-20:]

    # Translate back to selected language
    reply_final = await translator.from_en(reply_en, current_lang)

    # Return HTML that fits your chat.js
    return HTMLResponse(f"<div class='msg ai'><div class='bubble'>{reply_final}</div></div>")
