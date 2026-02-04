@echo off
echo ====================================
echo Cucina Italiana - Avvio Frontend
echo ====================================
echo.

cd /d %~dp0

echo Avvio server HTTP sulla porta 3000 (PowerShell HttpListener)...
echo.

REM Chiama lo script PowerShell (no Python richiesto)
powershell -ExecutionPolicy Bypass -File "%~dp0start.ps1"

REM Mantieni il terminale aperto
pause

