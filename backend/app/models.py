from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, relationship

from app.db import Base


class Genre(Base):
    __tablename__ = "generi"

    id: Mapped[int] = Column(Integer, primary_key=True)
    nome: Mapped[str] = Column(String(120), unique=True, nullable=False)
    descrizione: Mapped[str | None] = Column(Text)


recipe_genre = Table(
    "genere_ricette",
    Base.metadata,
    Column("genere_id", ForeignKey("generi.id"), primary_key=True),
    Column("ricetta_id", ForeignKey("ricette.id"), primary_key=True),
)


class Recipe(Base):
    __tablename__ = "ricette"

    id: Mapped[int] = Column(Integer, primary_key=True)
    titolo: Mapped[str] = Column(String(200), nullable=False)
    excerpt: Mapped[str | None] = Column(String(255))
    descrizione: Mapped[str | None] = Column(Text)
    tempo_minuti: Mapped[int | None] = Column(Integer)
    difficolta: Mapped[str | None] = Column(String(50))
    porzioni_default: Mapped[int] = Column(Integer, default=2)
    cover_url: Mapped[str | None] = Column(String(255))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    generi = relationship("Genre", secondary=recipe_genre, backref="ricette")
    ingredienti = relationship("RecipeIngredient", back_populates="ricetta")
    media = relationship("Media", back_populates="ricetta")
    vini = relationship("RecipeWine", back_populates="ricetta")

    def prezzo_base_porzione(self) -> Decimal:
        if not self.ingredienti:
            return Decimal("0.00")
        totale = sum((item.prezzo_per_porzione() for item in self.ingredienti), Decimal("0.00"))
        return totale.quantize(Decimal("0.01"))


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = Column(Integer, primary_key=True)
    ricetta_id: Mapped[int] = Column(Integer, ForeignKey("ricette.id"))
    url: Mapped[str] = Column(String(255), nullable=False)
    tipo: Mapped[str | None] = Column(String(50))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    ricetta = relationship("Recipe", back_populates="media")


class Ingredient(Base):
    __tablename__ = "ingredienti"

    id: Mapped[int] = Column(Integer, primary_key=True)
    nome: Mapped[str] = Column(String(120), unique=True, nullable=False)
    unita_base: Mapped[str] = Column(String(20), nullable=False)
    prezzo_per_unita: Mapped[Decimal] = Column(Numeric(10, 4), nullable=False)

    ricette = relationship("RecipeIngredient", back_populates="ingrediente")


class RecipeIngredient(Base):
    __tablename__ = "ricetta_ingredienti"
    __table_args__ = (UniqueConstraint("ricetta_id", "ingrediente_id", name="uq_ricetta_ingrediente"),)

    id: Mapped[int] = Column(Integer, primary_key=True)
    ricetta_id: Mapped[int] = Column(Integer, ForeignKey("ricette.id"))
    ingrediente_id: Mapped[int] = Column(Integer, ForeignKey("ingredienti.id"))
    quantita_per_persona: Mapped[Decimal] = Column(Numeric(10, 4), nullable=False)
    unita_misura: Mapped[str] = Column(String(20), nullable=False)

    ricetta = relationship("Recipe", back_populates="ingredienti")
    ingrediente = relationship("Ingredient", back_populates="ricette")

    def prezzo_per_porzione(self) -> Decimal:
        base_qty = convert_to_base_unit(self.quantita_per_persona, self.unita_misura, self.ingrediente.unita_base)
        return (base_qty * Decimal(self.ingrediente.prezzo_per_unita)).quantize(Decimal("0.01"))


class Wine(Base):
    __tablename__ = "vini"

    id: Mapped[int] = Column(Integer, primary_key=True)
    nome: Mapped[str] = Column(String(120), nullable=False)
    regione: Mapped[str | None] = Column(String(120))
    prezzo: Mapped[Decimal | None] = Column(Numeric(10, 2))

    ricette = relationship("RecipeWine", back_populates="vino")


class RecipeWine(Base):
    __tablename__ = "ricetta_vini"
    __table_args__ = (UniqueConstraint("ricetta_id", "vino_id", name="uq_ricetta_vino"),)

    id: Mapped[int] = Column(Integer, primary_key=True)
    ricetta_id: Mapped[int] = Column(Integer, ForeignKey("ricette.id"))
    vino_id: Mapped[int] = Column(Integer, ForeignKey("vini.id"))

    ricetta = relationship("Recipe", back_populates="vini")
    vino = relationship("Wine", back_populates="ricette")


class User(Base):
    __tablename__ = "utenti"

    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(80), unique=True, nullable=False)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = Column(String(255), nullable=False)
    is_admin: Mapped[bool] = Column(Boolean, default=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)


class RecipeScore(Base):
    __tablename__ = "punteggi_ricette"
    __table_args__ = (UniqueConstraint("ricetta_id", "utente_id", name="uq_punteggio_utente"),)

    id: Mapped[int] = Column(Integer, primary_key=True)
    ricetta_id: Mapped[int] = Column(Integer, ForeignKey("ricette.id"))
    utente_id: Mapped[int] = Column(Integer, ForeignKey("utenti.id"))
    punteggio: Mapped[int] = Column(Integer, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)


class SavedRecipe(Base):
    __tablename__ = "salva_ricette"
    __table_args__ = (UniqueConstraint("ricetta_id", "utente_id", name="uq_salva_ricetta"),)

    id: Mapped[int] = Column(Integer, primary_key=True)
    ricetta_id: Mapped[int] = Column(Integer, ForeignKey("ricette.id"))
    utente_id: Mapped[int] = Column(Integer, ForeignKey("utenti.id"))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)


class Cart(Base):
    __tablename__ = "carrelli"

    id: Mapped[int] = Column(Integer, primary_key=True)
    utente_id: Mapped[int] = Column(Integer, ForeignKey("utenti.id"))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    items = relationship("CartItem", back_populates="carrello")


class CartItem(Base):
    __tablename__ = "carrello_items"

    id: Mapped[int] = Column(Integer, primary_key=True)
    carrello_id: Mapped[int] = Column(Integer, ForeignKey("carrelli.id"))
    ricetta_id: Mapped[int] = Column(Integer, ForeignKey("ricette.id"))
    vino_id: Mapped[int | None] = Column(Integer, ForeignKey("vini.id"))
    persone: Mapped[int] = Column(Integer, default=2)
    prezzo_item: Mapped[Decimal] = Column(Numeric(10, 2), nullable=False)

    carrello = relationship("Cart", back_populates="items")


class Order(Base):
    __tablename__ = "ordini"

    id: Mapped[int] = Column(Integer, primary_key=True)
    utente_id: Mapped[int] = Column(Integer, ForeignKey("utenti.id"))
    stato: Mapped[str] = Column(String(50), default="in_attesa")
    indirizzo_consegna: Mapped[str] = Column(String(255))
    totale: Mapped[Decimal] = Column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    ricette = relationship("OrderRecipe", back_populates="ordine")


class OrderRecipe(Base):
    __tablename__ = "ordine_ricette"

    id: Mapped[int] = Column(Integer, primary_key=True)
    ordine_id: Mapped[int] = Column(Integer, ForeignKey("ordini.id"))
    ricetta_id: Mapped[int] = Column(Integer, ForeignKey("ricette.id"))
    persone: Mapped[int] = Column(Integer, nullable=False)
    prezzo_snapshot: Mapped[Decimal] = Column(Numeric(10, 2), nullable=False)

    ordine = relationship("Order", back_populates="ricette")


CONVERSION_MAP = {
    ("g", "kg"): Decimal("0.001"),
    ("kg", "g"): Decimal("1000"),
    ("ml", "l"): Decimal("0.001"),
    ("l", "ml"): Decimal("1000"),
}


def convert_to_base_unit(qty: Decimal, unit: str, base_unit: str) -> Decimal:
    if unit == base_unit:
        return qty
    factor = CONVERSION_MAP.get((unit, base_unit))
    if factor is None:
        raise ValueError(f"Unsupported conversion: {unit} -> {base_unit}")
    return (qty * factor).quantize(Decimal("0.0001"))
