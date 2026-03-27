from app.main import app
from app.routers import auth, resume, chat, dashboard, company

app.include_router(chat.router)
app.include_router(resume.router)
app.include_router(dashboard.router)


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Placement AI Hub is running!")
    print("👉 http://127.0.0.1:8000\n")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
