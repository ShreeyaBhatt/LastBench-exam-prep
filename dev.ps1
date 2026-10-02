# Development mode: FastAPI with auto-reload on :8000 and Vite with hot reload on :5173.
$root = $PSScriptRoot
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; python -m uvicorn app.main:app --reload --port 8000"
Push-Location "$root\frontend"
try { npm run dev } finally { Pop-Location }
