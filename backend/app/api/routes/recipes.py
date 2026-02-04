from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Recipe
from app.schemas import IngredientItem, RecipeDetail, RecipeListItem, WineItem

router = APIRouter(prefix="/ricette", tags=["ricette"])


@router.get("", response_model=List[RecipeListItem])

def list_recipes(
    q: Optional[str] = Query(default=None),
    genere: Optional[str] = Query(default=None),
    difficolta: Optional[str] = Query(default=None),
    tempo_max: Optional[int] = Query(default=None),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(Recipe)
    if q:
        query = query.filter(Recipe.titolo.ilike(f"%{q}%"))
    if difficolta:
        query = query.filter(Recipe.difficolta == difficolta)
    if tempo_max:
        query = query.filter(Recipe.tempo_minuti <= tempo_max)
    offset = (page - 1) * per_page
    recipes = query.offset(offset).limit(per_page).all()
    return [
        RecipeListItem(
            id=ricetta.id,
            titolo=ricetta.titolo,
            excerpt=ricetta.excerpt,
            cover_url=ricetta.cover_url,
            porzioni_default=ricetta.porzioni_default,
            tempo_minuti=ricetta.tempo_minuti,
        )
        for ricetta in recipes
    ]


@router.get("/{recipe_id}", response_model=RecipeDetail)

def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    ricetta = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not ricetta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ricetta non trovata")
    ingredienti = [
        IngredientItem(
            id=item.ingrediente.id,
            nome=item.ingrediente.nome,
            quantita_per_persona=item.quantita_per_persona,
            unita_misura=item.unita_misura,
        )
        for item in ricetta.ingredienti
    ]
    vini = [
        WineItem(
            id=item.vino.id,
            nome=item.vino.nome,
            prezzo=item.vino.prezzo,
        )
        for item in ricetta.vini
    ]
    return RecipeDetail(
        id=ricetta.id,
        titolo=ricetta.titolo,
        descrizione=ricetta.descrizione,
        porzioni_default=ricetta.porzioni_default,
        tempo_minuti=ricetta.tempo_minuti,
        ingredienti=ingredienti,
        vini=vini,
        prezzo_base_porzione=ricetta.prezzo_base_porzione(),
    )
