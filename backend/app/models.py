"""
Modelli SQLAlchemy per il database Cucina Italiana
Mappano lo schema esistente su Aiven MySQL
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    DECIMAL,
)
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, relationship

from app.db import Base


# ==================== GENERI ====================
class Genre(Base):
    """Tabella GENERI - Categorie delle ricette"""
    __tablename__ = "GENERI"
    __table_args__ = {'extend_existing': True}

    ID: Mapped[int] = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = Column("nome", String(80), unique=True, nullable=False)

    # Relazioni
    ricette = relationship("Recipe", secondary="GENERE_RICETTA", back_populates="generi")


# ==================== TABELLA ASSOCIATIVA GENERE_RICETTA ====================
genere_ricetta = Table(
    "GENERE_RICETTA",
    Base.metadata,
    Column("ID_GENERE", Integer, ForeignKey("GENERI.ID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("ID_RICETTA", Integer, ForeignKey("RICETTE.ID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    extend_existing=True
)


# ==================== RICETTE ====================
class Recipe(Base):
    """Tabella RICETTE"""
    __tablename__ = "RICETTE"
    __table_args__ = {'extend_existing': True}

    ID: Mapped[int] = Column("ID", Integer, primary_key=True, autoincrement=True)
    titolo: Mapped[str] = Column("titolo", String(150), nullable=False)
    descrizione: Mapped[str] = Column("descrizione", Text, nullable=False)
    porzioni_default: Mapped[int] = Column("porzioni_default", Integer, nullable=False, default=4)
    tempo_preparazione_min: Mapped[int | None] = Column("tempo_preparazione_min", Integer, nullable=True)
    difficolta: Mapped[str | None] = Column("difficolta", Enum('facile', 'media', 'difficile'), default='media')

    # Relazioni
    generi = relationship("Genre", secondary="GENERE_RICETTA", back_populates="ricette")
    ingredienti = relationship("RecipeIngredient", back_populates="ricetta", cascade="all, delete-orphan")
    media = relationship("Media", back_populates="ricetta", cascade="all, delete-orphan")
    vini = relationship("RecipeWine", back_populates="ricetta", cascade="all, delete-orphan")
    punteggi = relationship("RecipeScore", cascade="all, delete-orphan")
    salvataggi = relationship("SavedRecipe", cascade="all, delete-orphan")

    def prezzo_base_porzione(self) -> Decimal:
        """Calcola il prezzo base per porzione"""
        if not self.ingredienti:
            return Decimal("0.00")
        totale = sum((item.prezzo_per_porzione() for item in self.ingredienti), Decimal("0.00"))
        return totale.quantize(Decimal("0.01"))


# ==================== MEDIA ====================
class Media(Base):
    """Tabella MEDIA - Immagini e video per ricette"""
    __tablename__ = "MEDIA"
    __table_args__ = {'extend_existing': True}

    ID: Mapped[int] = Column("ID", Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = Column("url", Text, nullable=False)
    tipo: Mapped[str] = Column("tipo", String(50), nullable=False)
    ID_RICETTA: Mapped[int] = Column("ID_RICETTA", Integer, ForeignKey("RICETTE.ID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    # Relazioni
    ricetta = relationship("Recipe", back_populates="media")


# ==================== INGREDIENTI ====================
class Ingredient(Base):
    """Tabella INGREDIENTI"""
    __tablename__ = "INGREDIENTI"
    __table_args__ = {'extend_existing': True}

    ID: Mapped[int] = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = Column("nome", String(120), nullable=False)
    unita_base: Mapped[str] = Column("unita_base", String(20), nullable=False)
    prezzo_per_unita: Mapped[Decimal] = Column("prezzo_per_unita", DECIMAL(10, 2), nullable=False)

    # Relazioni
    ricette = relationship("RecipeIngredient", back_populates="ingrediente")


# ==================== RICETTA_INGREDIENTE ====================
class RecipeIngredient(Base):
    """Tabella RICETTA_INGREDIENTE - Ingredienti per ricetta"""
    __tablename__ = "RICETTA_INGREDIENTE"
    __table_args__ = {'extend_existing': True}

    ID_RICETTA: Mapped[int] = Column("ID_RICETTA", Integer, ForeignKey("RICETTE.ID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    ID_INGREDIENTE: Mapped[int] = Column("ID_INGREDIENTE", Integer, ForeignKey("INGREDIENTI.ID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    quantita_per_persona: Mapped[Decimal] = Column("quantita_per_persona", DECIMAL(10, 4), nullable=False)
    unita_misura: Mapped[str] = Column("unita_misura", String(20), nullable=False)

    # Relazioni
    ricetta = relationship("Recipe", back_populates="ingredienti")
    ingrediente = relationship("Ingredient", back_populates="ricette")

    def prezzo_per_porzione(self) -> Decimal:
        """Calcola il prezzo per porzione di questo ingrediente"""
        base_qty = convert_to_base_unit(self.quantita_per_persona, self.unita_misura, self.ingrediente.unita_base)
        return (base_qty * Decimal(self.ingrediente.prezzo_per_unita)).quantize(Decimal("0.01"))


# ==================== VINI ====================
class Wine(Base):
    """Tabella VINI"""
    __tablename__ = "VINI"
    __table_args__ = {'extend_existing': True}

    ID: Mapped[int] = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = Column("nome", String(150), nullable=False)
    descrizione: Mapped[str | None] = Column("descrizione", Text, nullable=True)
    tipo: Mapped[str | None] = Column("tipo", String(80), nullable=True)
    nazione: Mapped[str | None] = Column("nazione", String(80), nullable=True)
    regione: Mapped[str | None] = Column("regione", String(80), nullable=True)
    prezzo: Mapped[Decimal | None] = Column("prezzo", DECIMAL(10, 2), nullable=True)

    # Relazioni
    ricette = relationship("RecipeWine", back_populates="vino")


# ==================== RICETTA_VINO ====================
class RecipeWine(Base):
    """Tabella RICETTA_VINO - Vini consigliati per ricetta"""
    __tablename__ = "RICETTA_VINO"
    __table_args__ = {'extend_existing': True}

    ID_RICETTA: Mapped[int] = Column("ID_RICETTA", Integer, ForeignKey("RICETTE.ID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    ID_VINO: Mapped[int] = Column("ID_VINO", Integer, ForeignKey("VINI.ID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    annata: Mapped[int | None] = Column("annata", Integer, nullable=True)

    # Relazioni
    ricetta = relationship("Recipe", back_populates="vini")
    vino = relationship("Wine", back_populates="ricette")


# ==================== UTENTI ====================
class User(Base):
    """Tabella UTENTI"""
    __tablename__ = "UTENTI"
    __table_args__ = {'extend_existing': True}

    ID: Mapped[int] = Column("ID", Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = Column("username", String(60), unique=True, nullable=False)
    email: Mapped[str] = Column("email", String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = Column("password_hash", String(255), nullable=False)
    nome: Mapped[str | None] = Column("nome", String(100), nullable=True)
    cognome: Mapped[str | None] = Column("cognome", String(100), nullable=True)
    indirizzo: Mapped[str | None] = Column("indirizzo", Text, nullable=True)
    data_creazione: Mapped[datetime] = Column("data_creazione", DateTime, default=datetime.utcnow)

    # Relazioni
    carrelli = relationship("Cart", back_populates="utente")
    ordini = relationship("Order", back_populates="utente")


# ==================== PUNTEGGIO_RICETTA ====================
class RecipeScore(Base):
    """Tabella PUNTEGGIO_RICETTA - Valutazioni utenti"""
    __tablename__ = "PUNTEGGIO_RICETTA"
    __table_args__ = {'extend_existing': True}

    ID_UTENTE: Mapped[int] = Column("ID_UTENTE", Integer, ForeignKey("UTENTI.ID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    ID_RICETTA: Mapped[int] = Column("ID_RICETTA", Integer, ForeignKey("RICETTE.ID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    punteggio: Mapped[int] = Column("punteggio", TINYINT, nullable=False)


# ==================== SALVA_RICETTA ====================
class SavedRecipe(Base):
    """Tabella SALVA_RICETTA - Ricette salvate dall'utente"""
    __tablename__ = "SALVA_RICETTA"
    __table_args__ = {'extend_existing': True}

    ID_UTENTE: Mapped[int] = Column("ID_UTENTE", Integer, ForeignKey("UTENTI.ID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    ID_RICETTA: Mapped[int] = Column("ID_RICETTA", Integer, ForeignKey("RICETTE.ID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    data_salvataggio: Mapped[datetime] = Column("data_salvataggio", DateTime, default=datetime.utcnow)


# ==================== CARRELLI ====================
class Cart(Base):
    """Tabella CARRELLI"""
    __tablename__ = "CARRELLI"
    __table_args__ = {'extend_existing': True}

    ID: Mapped[int] = Column("ID", Integer, primary_key=True, autoincrement=True)
    ID_UTENTE: Mapped[int] = Column("ID_UTENTE", Integer, ForeignKey("UTENTI.ID", ondelete="CASCADE"), nullable=False)
    creato: Mapped[datetime] = Column("creato", DateTime, default=datetime.utcnow)
    aggiornato: Mapped[datetime] = Column("aggiornato", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relazioni
    utente = relationship("User", back_populates="carrelli")
    items = relationship("CartItem", back_populates="carrello", cascade="all, delete-orphan")


# ==================== CARRELLO_ITEM ====================
class CartItem(Base):
    """Tabella CARRELLO_ITEM - Elementi del carrello"""
    __tablename__ = "CARRELLO_ITEM"
    __table_args__ = {'extend_existing': True}

    ID: Mapped[int] = Column("ID", Integer, primary_key=True, autoincrement=True)
    ID_CARRELLO: Mapped[int] = Column("ID_CARRELLO", Integer, ForeignKey("CARRELLI.ID", ondelete="CASCADE"), nullable=False)
    ID_RICETTA: Mapped[int] = Column("ID_RICETTA", Integer, ForeignKey("RICETTE.ID", ondelete="CASCADE"), nullable=False)
    ID_VINO: Mapped[int | None] = Column("ID_VINO", Integer, ForeignKey("VINI.ID", ondelete="SET NULL"), nullable=True)
    persone: Mapped[int] = Column("persone", Integer, nullable=False, default=1)
    prezzo_item: Mapped[Decimal | None] = Column("prezzo_item", DECIMAL(10, 2), nullable=True)

    # Relazioni
    carrello = relationship("Cart", back_populates="items")
    recipe = relationship("Recipe", foreign_keys=[ID_RICETTA])
    wine = relationship("Wine", foreign_keys=[ID_VINO])


# ==================== ORDINI ====================
class Order(Base):
    """Tabella ORDINI"""
    __tablename__ = "ORDINI"
    __table_args__ = {'extend_existing': True}

    ID: Mapped[int] = Column("ID", Integer, primary_key=True, autoincrement=True)
    ID_UTENTE: Mapped[int] = Column("ID_UTENTE", Integer, ForeignKey("UTENTI.ID", ondelete="CASCADE"), nullable=False)
    totale: Mapped[Decimal] = Column("totale", DECIMAL(10, 2), nullable=False)
    data_ordine: Mapped[datetime] = Column("data_ordine", DateTime, default=datetime.utcnow)
    stato: Mapped[str] = Column("stato", Enum('creato', 'pagato', 'in_consegna', 'consegnato', 'annullato'), default='creato')
    indirizzo_consegna: Mapped[str | None] = Column("indirizzo_consegna", Text, nullable=True)

    # Relazioni
    utente = relationship("User", back_populates="ordini")
    ricette = relationship("OrderRecipe", back_populates="ordine", cascade="all, delete-orphan")


# ==================== ORDINE_RICETTA ====================
class OrderRecipe(Base):
    """Tabella ORDINE_RICETTA - Dettaglio ordini"""
    __tablename__ = "ORDINE_RICETTA"
    __table_args__ = {'extend_existing': True}

    ID_ORDINE: Mapped[int] = Column("ID_ORDINE", Integer, ForeignKey("ORDINI.ID", ondelete="CASCADE"), primary_key=True)
    ID_RICETTA: Mapped[int] = Column("ID_RICETTA", Integer, ForeignKey("RICETTE.ID", ondelete="CASCADE"), primary_key=True)
    ID_VINO: Mapped[int | None] = Column("ID_VINO", Integer, ForeignKey("VINI.ID", ondelete="SET NULL"), nullable=True)
    persone: Mapped[int] = Column("persone", Integer, nullable=False)
    prezzo_item: Mapped[Decimal] = Column("prezzo_item", DECIMAL(10, 2), nullable=False)

    # Relazioni
    ordine = relationship("Order", back_populates="ricette")


# ==================== UTILITÀ DI CONVERSIONE UNITÀ ====================
CONVERSION_MAP = {
    ("g", "kg"): Decimal("0.001"),
    ("kg", "g"): Decimal("1000"),
    ("ml", "l"): Decimal("0.001"),
    ("l", "ml"): Decimal("1000"),
}


def convert_to_base_unit(qty: Decimal, unit: str, base_unit: str) -> Decimal:
    """Converte una quantità da un'unità a un'altra"""
    if unit == base_unit:
        return qty
    factor = CONVERSION_MAP.get((unit, base_unit))
    if factor is None:
        raise ValueError(f"Conversione non supportata: {unit} -> {base_unit}")
    return (qty * factor).quantize(Decimal("0.0001"))
