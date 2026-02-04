# 🚀 QUICK START - Cucina Italiana

## 📋 CREDENZIALI TEST

### Utenti Database
```
User 1:
Email: mario.rossi@example.com
Password: password123
Nome: Mario Rossi

User 2:
Email: laura.bianchi@example.com
Password: password123
Nome: Laura Bianchi

User 3:
Email: giuseppe.verdi@example.com
Password: password123
Nome: Giuseppe Verdi
```

---

## ⚡ AVVIO RAPIDO

### Terminal 1 - Backend
```powershell
cd backend
.\start.ps1
```
**Output atteso:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```
**API Docs:** http://localhost:8000/docs

### Terminal 2 - Frontend
```powershell
cd frontend
.\start.ps1
```
**Output atteso:**
```
Server started on http://localhost:3000
Press Ctrl+C to stop
```
**App URL:** http://localhost:3000

---

## 🎯 TEST RAPIDO (2 MINUTI)

1. **Apri browser:** http://localhost:3000
2. **Login:** mario.rossi@example.com / password123
3. **Click su ricetta** → Vedi dettagli
4. **Aggiungi al carrello** → Scegli 4 persone
5. **Click Carrello** → Vedi item e totale
6. **Procedi al checkout** → Inserisci indirizzo
7. **Conferma ordine** → Vedi toast successo ✅

---

## 📊 RICETTE DISPONIBILI

```
1. Spaghetti alla Carbonara (Primi)
2. Bucatini all'Amatriciana (Primi)
3. Trofie al Pesto (Primi)
4. Cacio e Pepe (Primi)
5. Parmigiana di Melanzane (Secondi)
6. Tiramisù (Dolci)
```

---

## 🔗 LINK UTILI

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc

---

## 🛠️ COMANDI UTILI

### Popolare Database
```powershell
cd backend
python populate_db.py
```

### Reset Database
```powershell
cd backend
# Esegui lo schema SQL su Aiven
# Poi:
python populate_db.py
```

### Restart Backend
```powershell
# Premi Ctrl+C nel terminal backend
.\start.ps1
```

### Restart Frontend
```powershell
# Premi Ctrl+C nel terminal frontend
.\start.ps1
```

---

## 📱 ENDPOINTS API PRINCIPALI

### Pubblici (no auth)
```
GET  /api/recipes          - Lista ricette
GET  /api/recipes/{id}     - Dettaglio ricetta
GET  /api/recipes/genres   - Lista generi
POST /api/auth/login       - Login
POST /api/auth/register    - Registrazione
```

### Protetti (require auth)
```
GET    /api/cart             - Carrello utente
POST   /api/cart/items       - Aggiungi item
PATCH  /api/cart/items/{id}  - Modifica item
DELETE /api/cart/items/{id}  - Rimuovi item
POST   /api/cart/checkout    - Checkout
GET    /api/cart/orders      - Storico ordini
```

---

## 🎨 FEATURES IMPLEMENTATE

✅ **Autenticazione:** Login/Logout con JWT  
✅ **Catalogo:** 6 ricette con immagini Unsplash  
✅ **Dettagli:** Modal con ingredienti e vini  
✅ **Filtri:** Per genere (dinamici da API)  
✅ **Ricerca:** Client-side con debounce  
✅ **Carrello:** Aggiungi, rimuovi, visualizza  
✅ **Persone:** Modal per scegliere 1-20 persone  
✅ **Prezzi:** Calcolo dinamico per n persone  
✅ **Checkout:** Con indirizzo e transazione atomica  
✅ **Ordini:** Salvati in DB con snapshot prezzi  
✅ **UX:** Toast, modal, animazioni, no prompt/alert  

---

## 🐛 PROBLEMI COMUNI

### CORS Error
**Problema:** `Access-Control-Allow-Origin`  
**Soluzione:** Verifica che frontend sia su porta 3000 e backend su 8000

### Token Expired
**Problema:** 401 Unauthorized  
**Soluzione:** Logout → Login nuovamente

### Database Empty
**Problema:** Nessuna ricetta visualizzata  
**Soluzione:** `python populate_db.py`

### Port Already in Use
**Problema:** Porta 8000 o 3000 occupata  
**Soluzione:** 
```powershell
# Trova processo
netstat -ano | findstr :8000
# Termina processo
taskkill /PID <PID> /F
```

---

## 📞 SUPPORTO

### Logs Backend
Il terminal backend mostra tutti i log delle richieste:
```
INFO: 127.0.0.1:xxxxx - "GET /api/recipes HTTP/1.1" 200 OK
```

### Logs Frontend
Apri DevTools (F12) → Console per vedere:
- Errori JavaScript
- API calls
- Dati ricevuti

### Debug Database
Usa Aiven Console o MySQL client:
```bash
mysql -u user -p -h host -D cucina
```

---

## ✅ CHECKLIST PRIMA DEMO

- [ ] Backend avviato e risponde su :8000/docs
- [ ] Frontend avviato e carica su :3000
- [ ] Database popolato (6 ricette visibili)
- [ ] Login funziona con mario.rossi@example.com
- [ ] Carrello si aggiorna correttamente
- [ ] Checkout completa ordine
- [ ] Badge carrello si azzera dopo checkout

**Se tutti ✅ → Pronto per la demo! 🎉**

---

## 🎓 SPIEGAZIONE ARCHITETTURA

### Backend (FastAPI)
```
app/
├── api/routes/      # Endpoints modulari
│   ├── auth.py      # Login/Register
│   ├── recipes.py   # Catalogo ricette
│   └── cart.py      # Carrello e checkout
├── core/            # Configurazione
│   ├── config.py    # ENV variables
│   └── security.py  # JWT e password hashing
├── models.py        # Database ORM models
├── schemas.py       # Pydantic validation
├── services.py      # Business logic (prezzi)
└── db.py           # Database connection
```

### Frontend (Vanilla JS)
```
frontend/
├── index.html      # 5 modal integrate
├── styles.css      # Design moderno responsive
└── app.js          # Logic + API calls
```

### Database (MySQL Aiven)
```
16 tabelle:
- UTENTI, RICETTE, GENERI
- INGREDIENTI, VINI, MEDIA
- CARRELLI, CARRELLO_ITEM
- ORDINI, ORDINE_RICETTA
- Relazioni many-to-many
- Snapshot prezzi per storicità
```

---

**Buon test! 🚀**
