from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80, alias="nome")
    email: EmailStr
    password: str = Field(min_length=8)
    telefono: Optional[str] = None

    class Config:
        populate_by_name = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool


class RecipeListItem(BaseModel):
    ID: int
    titolo: str
    descrizione: Optional[str] = None
    main_image: Optional[str] = None
    tempo_preparazione: Optional[int] = None
    difficolta: Optional[str] = None

    class Config:
        from_attributes = True


class IngredientItem(BaseModel):
    id: int
    nome: str
    quantita_per_persona: Decimal
    unita_misura: str


class WineItem(BaseModel):
    id: int
    nome: str
    prezzo: Optional[Decimal]


class RecipeDetail(BaseModel):
    ID: int
    titolo: str
    descrizione: Optional[str] = None
    porzioni_default: Optional[int] = None
    tempo_preparazione: Optional[int] = None
    difficolta: Optional[str] = None
    ingredienti: List[IngredientItem] = []
    vini: List[WineItem] = []
    prezzo_base_porzione: Optional[Decimal] = None
    main_image: Optional[str] = None

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[dict]


# Cart schemas
class CartItemCreate(BaseModel):
    recipe_id: int
    persone: int = Field(ge=1, description="Numero di persone (minimo 1)")
    vino_id: Optional[int] = None


class CartItemUpdate(BaseModel):
    persone: int = Field(ge=1, description="Numero di persone (minimo 1)")


class CartItemResponse(BaseModel):
    ID: int
    recipe: RecipeListItem
    wine: Optional[WineItem]
    persone: int
    prezzo_item: Decimal

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    ID: int
    items: List[dict]
    totale: Decimal
    count: int


# Checkout schemas
class CheckoutRequest(BaseModel):
    indirizzo_consegna: str = Field(min_length=10, max_length=255)


class OrderResponse(BaseModel):
    ID: int
    ID_UTENTE: int
    totale: Decimal
    data_ordine: datetime
    stato: str
    indirizzo_consegna: Optional[str]
    num_ricette: int

    class Config:
        from_attributes = True
