# Cucina Italiana

Webapp per consultare e acquistare ricette complete con backend FastAPI e frontend HTML/JS.

## Struttura
- `backend/` API FastAPI, modelli SQLAlchemy, logica pricing.
- `frontend/` interfaccia statica minimale.

## Avvio rapido (dev)
```bash
docker-compose up --build
```

API disponibile su `http://localhost:8000`.

## Note
- Configurare `DATABASE_URL` e `JWT_SECRET` per ambienti reali.
- I modelli ORM seguono lo schema fornito e includono utilità di conversione unità.
