from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool


class RecipeListItem(BaseModel):
    id: int
    titolo: str
    excerpt: Optional[str]
    cover_url: Optional[str]
    porzioni_default: int
    tempo_minuti: Optional[int]


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
    id: int
    titolo: str
    descrizione: Optional[str]
    porzioni_default: int
    tempo_minuti: Optional[int]
    ingredienti: List[IngredientItem]
    vini: List[WineItem]
    prezzo_base_porzione: Decimal


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[dict]
