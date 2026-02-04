@echo off
echo ====================================
echo Cucina Italiana - Avvio Backend
echo ====================================
echo.

cd /d %~dp0

if not exist "venv" (
    echo Creazione ambiente virtuale...
    python -m venv venv
    echo.
)

echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo Installazione dipendenze...
pip install -r requirements.txt --quiet

echo.
echo Test connessione database...
python test_connection.py

echo.
echo ====================================
echo Avvio server FastAPI...
echo API disponibile su http://localhost:8000
echo Documentazione API su http://localhost:8000/docs
echo ====================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
