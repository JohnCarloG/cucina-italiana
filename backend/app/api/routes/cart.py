"""
API Endpoints per gestione carrello e checkout
"""
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.security import get_current_user
from app.db import get_db
from app.models import Cart, CartItem, Order, OrderRecipe, Recipe, User, Wine
from app.schemas import (
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
    CheckoutRequest,
    OrderResponse,
)
from app.services import calculate_recipe_price

router = APIRouter(prefix="/cart", tags=["cart"])


def get_or_create_cart(user_id: int, db: Session) -> Cart:
    """Recupera il carrello attivo dell'utente o ne crea uno nuovo"""
    cart = db.query(Cart).filter(Cart.ID_UTENTE == user_id).first()
    if not cart:
        cart = Cart(ID_UTENTE=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Recupera il carrello dell'utente autenticato con tutti gli items"""
    cart = get_or_create_cart(current_user.ID, db)
    
    # Carica items con ricette e vini
    items = (
        db.query(CartItem)
        .filter(CartItem.ID_CARRELLO == cart.ID)
        .options(
            joinedload(CartItem.recipe),
            joinedload(CartItem.wine)
        )
        .all()
    )
    
    # Calcola totale
    totale = sum((item.prezzo_item for item in items if item.prezzo_item), Decimal("0.00"))
    
    return CartResponse(
        ID=cart.ID,
        items=[
            {
                "ID": item.ID,
                "recipe": {
                    "ID": item.recipe.ID,
                    "titolo": item.recipe.titolo,
                    "descrizione": item.recipe.descrizione[:100] if item.recipe.descrizione else "",
                    "tempo_preparazione": item.recipe.tempo_preparazione_min,
                    "difficolta": item.recipe.difficolta,
                },
                "wine": {
                    "ID": item.wine.ID,
                    "nome": item.wine.nome,
                } if item.ID_VINO and item.wine else None,
                "persone": item.persone,
                "prezzo_item": item.prezzo_item,
            }
            for item in items
        ],
        totale=totale,
        count=len(items),
    )


@router.post("/items", status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    payload: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Aggiunge una ricetta al carrello con numero persone e vino opzionale"""
    # Verifica che la ricetta esista
    ricetta = db.query(Recipe).filter(Recipe.ID == payload.recipe_id).first()
    if not ricetta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ricetta non trovata"
        )
    
    # Verifica numero persone valido
    if payload.persone < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Il numero di persone deve essere almeno 1"
        )
    
    # Verifica vino se specificato
    vino = None
    if payload.vino_id:
        vino = db.query(Wine).filter(Wine.ID == payload.vino_id).first()
        if not vino:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vino non trovato"
            )
    
    # Calcola prezzo usando il service
    try:
        prezzo = calculate_recipe_price(ricetta, payload.persone, vino)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Recupera o crea carrello
    cart = get_or_create_cart(current_user.ID, db)
    
    # Verifica se item già presente (stessa ricetta e vino)
    existing_item = (
        db.query(CartItem)
        .filter(
            CartItem.ID_CARRELLO == cart.ID,
            CartItem.ID_RICETTA == payload.recipe_id,
            CartItem.ID_VINO == payload.vino_id if payload.vino_id else CartItem.ID_VINO.is_(None),
        )
        .first()
    )
    
    if existing_item:
        # Aggiorna persone e prezzo
        existing_item.persone = payload.persone
        existing_item.prezzo_item = prezzo
    else:
        # Crea nuovo item
        cart_item = CartItem(
            ID_CARRELLO=cart.ID,
            ID_RICETTA=payload.recipe_id,
            ID_VINO=payload.vino_id,
            persone=payload.persone,
            prezzo_item=prezzo,
        )
        db.add(cart_item)
    
    db.commit()
    
    return {
        "message": "Ricetta aggiunta al carrello",
        "prezzo_calcolato": float(prezzo),
    }


@router.patch("/items/{item_id}")
async def update_cart_item(
    item_id: int,
    payload: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Modifica il numero di persone di un item del carrello"""
    # Recupera carrello utente
    cart = get_or_create_cart(current_user.ID, db)
    
    # Trova item
    item = (
        db.query(CartItem)
        .filter(
            CartItem.ID == item_id,
            CartItem.ID_CARRELLO == cart.ID,
        )
        .options(joinedload(CartItem.recipe), joinedload(CartItem.wine))
        .first()
    )
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item non trovato nel carrello"
        )
    
    # Verifica numero persone valido
    if payload.persone < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Il numero di persone deve essere almeno 1"
        )
    
    # Ricalcola prezzo
    try:
        prezzo = calculate_recipe_price(item.recipe, payload.persone, item.wine)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Aggiorna
    item.persone = payload.persone
    item.prezzo_item = prezzo
    db.commit()
    
    return {
        "message": "Carrello aggiornato",
        "nuovo_prezzo": float(prezzo),
    }


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Rimuove un item dal carrello"""
    cart = get_or_create_cart(current_user.ID, db)
    
    item = (
        db.query(CartItem)
        .filter(
            CartItem.ID == item_id,
            CartItem.ID_CARRELLO == cart.ID,
        )
        .first()
    )
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item non trovato nel carrello"
        )
    
    db.delete(item)
    db.commit()
    
    return None


@router.post("/checkout", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def checkout(
    payload: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Crea un ordine dal carrello corrente.
    Transazione atomica: crea ordine, copia items, svuota carrello.
    """
    # Recupera carrello con items
    cart = get_or_create_cart(current_user.ID, db)
    items = (
        db.query(CartItem)
        .filter(CartItem.ID_CARRELLO == cart.ID)
        .options(joinedload(CartItem.recipe))
        .all()
    )
    
    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Il carrello è vuoto"
        )
    
    # Calcola totale
    totale = sum((item.prezzo_item for item in items if item.prezzo_item), Decimal("0.00"))
    
    if totale <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Totale ordine non valido"
        )
    
    try:
        # 1. Crea ordine
        order = Order(
            ID_UTENTE=current_user.ID,
            totale=totale,
            stato="creato",
            indirizzo_consegna=payload.indirizzo_consegna,
        )
        db.add(order)
        db.flush()  # Ottieni ID ordine senza commit
        
        # 2. Copia items nel dettaglio ordine (snapshot prezzi)
        for item in items:
            order_recipe = OrderRecipe(
                ID_ORDINE=order.ID,
                ID_RICETTA=item.ID_RICETTA,
                ID_VINO=item.ID_VINO,
                persone=item.persone,
                prezzo_item=item.prezzo_item,
            )
            db.add(order_recipe)
        
        # 3. Svuota carrello
        db.query(CartItem).filter(CartItem.ID_CARRELLO == cart.ID).delete()
        
        # 4. Commit transazione
        db.commit()
        db.refresh(order)
        
        return OrderResponse(
            ID=order.ID,
            ID_UTENTE=order.ID_UTENTE,
            totale=order.totale,
            data_ordine=order.data_ordine,
            stato=order.stato,
            indirizzo_consegna=order.indirizzo_consegna,
            num_ricette=len(items),
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Errore durante la creazione dell'ordine: {str(e)}"
        )


@router.get("/orders", response_model=List[OrderResponse])
async def get_user_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Recupera tutti gli ordini dell'utente autenticato"""
    orders = (
        db.query(Order)
        .filter(Order.ID_UTENTE == current_user.ID)
        .order_by(Order.data_ordine.desc())
        .all()
    )
    
    return [
        OrderResponse(
            ID=order.ID,
            ID_UTENTE=order.ID_UTENTE,
            totale=order.totale,
            data_ordine=order.data_ordine,
            stato=order.stato,
            indirizzo_consegna=order.indirizzo_consegna,
            num_ricette=len(order.ricette) if order.ricette else 0,
        )
        for order in orders
    ]
