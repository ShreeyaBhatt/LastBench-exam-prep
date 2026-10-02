# Starts LastBench at http://localhost:8000 (backend + built frontend).
# First run installs dependencies and builds the frontend.
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

if (-not (Test-Path "$root\frontend\node_modules")) {
    Write-Host "Installing frontend packages..."
    Push-Location "$root\frontend"; npm install; Pop-Location
}
if (-not (Test-Path "$root\frontend\dist\index.html") -or $args -contains "-rebuild") {
    Write-Host "Building frontend..."
    Push-Location "$root\frontend"; npm run build; Pop-Location
}

python -c "import fastapi, uvicorn, multipart, pymupdf, reportlab, anthropic" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing backend packages..."
    python -m pip install -r "$root\backend\requirements.txt"
}

Write-Host ""
Write-Host "LastBench is running at http://localhost:8000  (Ctrl+C to stop)"
Push-Location "$root\backend"
try { python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 }
finally { Pop-Location }
