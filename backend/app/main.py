from fastapi import FastAPI

from app.api.routes import auth, recipes, users

app = FastAPI(title="Cucina Italiana API", version="0.1.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(recipes.router)


@app.get("/health")

def health_check():
    return {"status": "ok"}
