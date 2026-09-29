# Vaani Setu

## Backend setup

From the `backend` directory:

```powershell
..\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Health check: `GET /health`.
