# 🚀 Come Avviare Cucina Italiana

## 📦 Requisiti
- Python 3.10+
- Database MySQL su Aiven (con tabelle già create)

---

## 🎯 Avvio Rapido

### 1️⃣ **Backend (API)**

Apri un terminale PowerShell:

```powershell
cd backend
.\start.ps1
```

✅ Backend disponibile su: **http://localhost:8000**
📚 API Docs: **http://localhost:8000/docs**

---

### 2️⃣ **Frontend (Interfaccia Web)**

Apri un **NUOVO** terminale PowerShell (separato dal backend):

```powershell
cd frontend
.\start.ps1
```

🎉 **Il browser si aprirà automaticamente su `http://localhost:3000/index.html`!**

> **Nota:** Lo script avvia il server e apre automaticamente il browser alla pagina corretta.

---

## 🌐 URL Completi

| Servizio | URL | Descrizione |
|----------|-----|-------------|
| **API Backend** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Documentazione Swagger |
| **Health Check** | http://localhost:8000/health | Status API |
| **Frontend** | http://localhost:3000/index.html | Interfaccia Web |

---

## 🛑 Come Fermare

- **Backend:** Premi `CTRL+C` nel terminale backend
- **Frontend:** Premi `CTRL+C` nel terminale frontend

---

## 📝 Metodo Alternativo (Manuale)

### Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```powershell
cd frontend
python -m http.server 3000
```
Poi: **http://localhost:3000/index.html**

---

## ⚠️ Troubleshooting

### Frontend mostra solo lista file
✅ **Soluzione:** Vai su `http://localhost:3000/index.html` invece di `http://localhost:3000`

### Errore CORS nel frontend
✅ **Soluzione:** Usa il server HTTP Python invece di aprire direttamente il file

### Backend non si avvia
✅ **Verifica:** 
- File `.env` configurato con credenziali Aiven
- Tabelle create su Aiven (esegui `schema.sql`)
- Dipendenze installate (`pip install -r requirements.txt`)

### Porta già in uso
✅ **Backend:** Cambia porta con `uvicorn app.main:app --reload --port 8080`
✅ **Frontend:** Cambia porta con `python -m http.server 3001`

---

## 🎉 Tutto Pronto!

Con entrambi i server avviati puoi:
1. ✅ Testare l'API su http://localhost:8000/docs
2. ✅ Usare l'interfaccia web su http://localhost:3000/index.html
3. ✅ Sviluppare nuove funzionalità

Buon lavoro! 🍝
