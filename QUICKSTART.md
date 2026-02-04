# 🍝 Cucina Italiana - Guida Rapida

## ✅ Modifiche Completate

### Rimosso
- ❌ Docker e Docker Compose
- ❌ SQLite
- ❌ Dockerfile
- ❌ docker-compose.yml

### Aggiunto
- ✅ Configurazione per MySQL Aiven
- ✅ Script di avvio automatici (start.ps1 / start.bat)
- ✅ File .env.example con template
- ✅ Guida configurazione Aiven (AIVEN_SETUP.md)
- ✅ Script init_db.py migliorato
- ✅ .gitignore completo
- ✅ README.md aggiornato

## 🚀 Come Avviare il Progetto

### 1. Configura il Database Aiven

Modifica il file `backend/.env` e inserisci le tue credenziali Aiven:

```env
DATABASE_URL=mysql+pymysql://username:password@host:port/database
JWT_SECRET=your-secret-key-change-this
```

📖 **Guida completa:** Vedi `AIVEN_SETUP.md`

### 2. Avvia il Backend

#### Metodo Rapido (PowerShell):
```powershell
cd backend
.\start.ps1
```

#### Metodo Manuale:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Apri il Frontend

```powershell
cd frontend
\.\start.ps1   # usa HttpListener integrato, non richiede Python
```

Il browser si aprirà automaticamente! 🎉

> Se vedi "Accesso negato" esegui PowerShell come **Amministratore** una sola volta e lancia:
> ```powershell
> netsh http add urlacl url=http://localhost:3000/ user=%USERDOMAIN%\%USERNAME%
> ```
> Poi riavvia `start.ps1`.

Oppure manualmente (senza Python):
```powershell
cd frontend
powershell -ExecutionPolicy Bypass -Command "l=New-Object System.Net.HttpListener; l.Prefixes.Add('http://localhost:3000/'); l.Start(); while(l.IsListening){c=l.GetContext();p=c.Request.Url.AbsolutePath.TrimStart('/'); if([string]::IsNullOrWhiteSpace(p)){p='index.html'}; f=Join-Path (Get-Location) p; if(Test-Path f){b=[IO.File]::ReadAllBytes(f); c.Response.OutputStream.Write(b,0,b.Length)} else {c.Response.StatusCode=404}; c.Response.Close()}"
```
Poi vai su: **http://localhost:3000/index.html**

## 📍 URL Utili

- **API:** http://localhost:8000
- **Documentazione API:** http://localhost:8000/docs
- **Frontend:** http://localhost:3000/index.html (si apre automaticamente)

## 🔧 Struttura Progetto

```
cucina-italiana/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # Endpoints API
│   │   ├── core/            # Configurazione
│   │   ├── models.py        # Modelli database
│   │   ├── schemas.py       # Validazione dati
│   │   ├── services.py      # Logica business
│   │   └── main.py          # Entry point FastAPI
│   ├── tests/               # Test unitari
│   ├── .env                 # Configurazione (NON committare!)
│   ├── .env.example         # Template configurazione
│   ├── requirements.txt     # Dipendenze Python
│   ├── init_db.py          # Inizializza database
│   ├── start.ps1           # Script avvio PowerShell
│   └── start.bat           # Script avvio CMD
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── README.md               # Documentazione completa
├── AIVEN_SETUP.md         # Guida Aiven
└── .gitignore

```

## 🎯 Prossimi Passi

1. **Configura Aiven**: Segui la guida in `AIVEN_SETUP.md`
2. **Inserisci le credenziali**: Modifica `backend/.env`
3. **Avvia il backend**: Esegui `.\start.ps1`
4. **Testa l'API**: Vai su http://localhost:8000/docs
5. **Apri il frontend**: Carica `index.html` nel browser

## 📚 Documentazione

- **README.md** - Documentazione completa del progetto
- **AIVEN_SETUP.md** - Guida configurazione database Aiven
- **backend/app/** - Codice sorgente con commenti

## 🆘 Supporto

In caso di problemi:
1. Controlla `AIVEN_SETUP.md` sezione Troubleshooting
2. Verifica che tutte le dipendenze siano installate
3. Controlla i log del server per errori specifici

---

**Nota**: Ricorda di non committare il file `.env` con le credenziali reali!
