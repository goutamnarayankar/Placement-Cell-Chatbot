# Activate virtual env and run FastAPI automatically

Write-Host "🔄 Activating virtual environment..."
.\venv\Scripts\activate

Write-Host "🚀 Starting Placement AI Hub..."
uvicorn app.main:app --reload --port 8000
