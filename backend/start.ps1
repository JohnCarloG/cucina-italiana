# Script di avvio per PowerShell
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Cucina Italiana - Avvio Backend" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

if (-not (Test-Path "venv")) {
    Write-Host "Creazione ambiente virtuale..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host ""
}

Write-Host "Attivazione ambiente virtuale..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Installazione dipendenze..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

Write-Host ""
Write-Host "Test connessione database..." -ForegroundColor Yellow
python test_connection.py

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "Avvio server FastAPI..." -ForegroundColor Green
Write-Host "API disponibile su http://localhost:8000" -ForegroundColor Green
Write-Host "Documentazione API su http://localhost:8000/docs" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
