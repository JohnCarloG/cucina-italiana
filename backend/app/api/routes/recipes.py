from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.db import get_db
from app.models import Recipe, Genre, RecipeIngredient, RecipeWine, Media
from app.schemas import IngredientItem, RecipeDetail, RecipeListItem, WineItem

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("", response_model=List[RecipeListItem])
def list_recipes(
    q: Optional[str] = Query(default=None),
    genre_id: Optional[int] = Query(default=None),
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
        query = query.filter(Recipe.tempo_preparazione <= tempo_max)
    # Note: genre filtering would need JOIN with GENERE_RICETTA table
    offset = (page - 1) * per_page
    recipes = query.offset(offset).limit(per_page).all()
    
    # Carica immagine principale per ogni ricetta
    result = []
    for ricetta in recipes:
        main_image_url = None
        media = db.query(Media).filter(
            Media.ID_RICETTA == ricetta.ID,
            Media.tipo == 'immagine'
        ).first()
        if media:
            main_image_url = media.url
        
        result.append(
            RecipeListItem(
                ID=ricetta.ID,
                titolo=ricetta.titolo,
                descrizione=ricetta.descrizione[:100] if ricetta.descrizione else "",
                main_image=main_image_url,
                tempo_preparazione=ricetta.tempo_preparazione_min,
                difficolta=ricetta.difficolta,
            )
        )
    
    return result


@router.get("/search", response_model=List[RecipeListItem])
def search_recipes(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    """Search recipes by title"""
    recipes = db.query(Recipe).filter(Recipe.titolo.ilike(f"%{q}%")).limit(20).all()
    return [
        RecipeListItem(
            ID=ricetta.ID,
            titolo=ricetta.titolo,
            descrizione=ricetta.descrizione[:100] if ricetta.descrizione else "",
            main_image=None,
            tempo_preparazione=ricetta.tempo_preparazione,
            difficolta=ricetta.difficolta,
        )
        for ricetta in recipes
    ]


@router.get("/genres")
def list_genres(db: Session = Depends(get_db)):
    """Get all recipe genres"""
    genres = db.query(Genre).all()
    return [{"ID": g.ID, "nome": g.nome} for g in genres]


@router.get("/{recipe_id}", response_model=RecipeDetail)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    ricetta = (
        db.query(Recipe)
        .options(
            joinedload(Recipe.ingredienti).joinedload(RecipeIngredient.ingrediente),
            joinedload(Recipe.vini).joinedload(RecipeWine.vino)
        )
        .filter(Recipe.ID == recipe_id)
        .first()
    )
    
    if not ricetta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ricetta non trovata")
    
    # Carica ingredienti con quantità per persona
    ingredienti_list = []
    for ri in ricetta.ingredienti:
        if ri.ingrediente:
            ingredienti_list.append(
                IngredientItem(
                    id=ri.ingrediente.ID,
                    nome=ri.ingrediente.nome,
                    quantita_per_persona=ri.quantita_per_persona or Decimal("0"),
                    unita_misura=ri.unita_misura or "kg",
                )
            )
    
    # Carica vini con prezzo
    vini_list = []
    for rv in ricetta.vini:
        if rv.vino:
            vini_list.append(
                WineItem(
                    id=rv.vino.ID,
                    nome=rv.vino.nome,
                    prezzo=rv.vino.prezzo if hasattr(rv.vino, 'prezzo') else None,
                )
            )
    
    # Calcola prezzo base per porzione
    try:
        prezzo_base = ricetta.prezzo_base_porzione() if ricetta.ingredienti else None
    except Exception:
        prezzo_base = None
    
    # Carica immagine principale
    main_image_url = None
    media = db.query(Media).filter(
        Media.ID_RICETTA == ricetta.ID,
        Media.tipo == 'immagine'
    ).first()
    if media:
        main_image_url = media.url
    
    return RecipeDetail(
        ID=ricetta.ID,
        titolo=ricetta.titolo,
        descrizione=ricetta.descrizione,
        porzioni_default=ricetta.porzioni_default,
        tempo_preparazione=ricetta.tempo_preparazione_min,
        difficolta=ricetta.difficolta,
        ingredienti=ingredienti_list,
        vini=vini_list,
        prezzo_base_porzione=prezzo_base,
        main_image=main_image_url,
    )
