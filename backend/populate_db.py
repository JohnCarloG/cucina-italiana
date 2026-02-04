"""
Script per popolare il database con dati di esempio
Ricette autentiche da lacucinaitaliana.it con ingredienti, vini, immagini e utenti di test
"""
import sys
from pathlib import Path

# Aggiungi la directory backend al path
sys.path.append(str(Path(__file__).parent))

from decimal import Decimal
from sqlalchemy.orm import Session
from app.db import engine, get_db
from app.models import (
    Genre, Recipe, Ingredient, RecipeIngredient, Wine, RecipeWine, 
    Media, User, genere_ricetta
)
from app.core.security import hash_password


def populate_database():
    """Popola il database con dati di esempio"""
    db = next(get_db())
    
    try:
        print("🍝 Inizio popolamento database Cucina Italiana...")
        
        # 0. UTENTI DI TEST
        print("\n👥 Creazione utenti di test...")
        utenti_data = [
            {
                "username": "mariorossi",
                "nome": "Mario",
                "cognome": "Rossi",
                "email": "mario.rossi@example.com",
                "password": "password123",
                "indirizzo": "Via Roma 1, 20100 Milano"
            },
            {
                "username": "laurabianchi",
                "nome": "Laura",
                "cognome": "Bianchi",
                "email": "laura.bianchi@example.com",
                "password": "password123",
                "indirizzo": "Corso Italia 45, 00100 Roma"
            },
            {
                "username": "giuseppeverdi",
                "nome": "Giuseppe",
                "cognome": "Verdi",
                "email": "giuseppe.verdi@example.com",
                "password": "password123",
                "indirizzo": "Piazza Duomo 10, 50100 Firenze"
            },
        ]
        
        for u_data in utenti_data:
            existing = db.query(User).filter(User.email == u_data["email"]).first()
            if not existing:
                user = User(
                    username=u_data["username"],
                    nome=u_data["nome"],
                    cognome=u_data.get("cognome"),
                    email=u_data["email"],
                    password_hash=hash_password(u_data["password"]),
                    indirizzo=u_data.get("indirizzo"),
                )
                db.add(user)
                db.flush()
                print(f"  ✓ Utente: {u_data['nome']} {u_data.get('cognome', '')} ({u_data['email']})")
            else:
                print(f"  → Utente esistente: {u_data['email']}")
        
        db.commit()
        
        # 1. GENERI
        print("\n📚 Creazione generi...")
        generi_data = [
            {"nome": "Primi Piatti"},
            {"nome": "Secondi Piatti"},
            {"nome": "Antipasti"},
            {"nome": "Dolci"},
            {"nome": "Contorni"},
            {"nome": "Pizze e Focacce"},
            {"nome": "Salse e Condimenti"},
            {"nome": "Zuppe e Minestre"},
        ]
        
        generi = {}
        for g_data in generi_data:
            existing = db.query(Genre).filter(Genre.nome == g_data["nome"]).first()
            if not existing:
                genere = Genre(**g_data)
                db.add(genere)
                db.flush()
                generi[g_data["nome"]] = genere
                print(f"  ✓ Genere: {g_data['nome']}")
            else:
                generi[g_data["nome"]] = existing
                print(f"  → Genere esistente: {g_data['nome']}")
        
        db.commit()
        
        # 2. INGREDIENTI
        print("\n🥬 Creazione ingredienti...")
        ingredienti_data = [
            # Pasta e cereali
            {"nome": "Spaghetti", "unita_base": "kg", "prezzo_per_unita": Decimal("2.50")},
            {"nome": "Penne rigate", "unita_base": "kg", "prezzo_per_unita": Decimal("2.30")},
            {"nome": "Riso Carnaroli", "unita_base": "kg", "prezzo_per_unita": Decimal("4.50")},
            {"nome": "Farina 00", "unita_base": "kg", "prezzo_per_unita": Decimal("1.20")},
            
            # Proteine
            {"nome": "Guanciale", "unita_base": "kg", "prezzo_per_unita": Decimal("18.00")},
            {"nome": "Pancetta", "unita_base": "kg", "prezzo_per_unita": Decimal("12.00")},
            {"nome": "Parmigiano Reggiano", "unita_base": "kg", "prezzo_per_unita": Decimal("25.00")},
            {"nome": "Pecorino Romano", "unita_base": "kg", "prezzo_per_unita": Decimal("22.00")},
            {"nome": "Mozzarella di bufala", "unita_base": "kg", "prezzo_per_unita": Decimal("14.00")},
            {"nome": "Uova", "unita_base": "pz", "prezzo_per_unita": Decimal("0.35")},
            {"nome": "Filetto di manzo", "unita_base": "kg", "prezzo_per_unita": Decimal("35.00")},
            
            # Verdure
            {"nome": "Pomodori pelati", "unita_base": "kg", "prezzo_per_unita": Decimal("3.50")},
            {"nome": "Pomodorini", "unita_base": "kg", "prezzo_per_unita": Decimal("4.20")},
            {"nome": "Basilico fresco", "unita_base": "g", "prezzo_per_unita": Decimal("0.02")},
            {"nome": "Aglio", "unita_base": "g", "prezzo_per_unita": Decimal("0.01")},
            {"nome": "Cipolla", "unita_base": "kg", "prezzo_per_unita": Decimal("1.50")},
            {"nome": "Zucchine", "unita_base": "kg", "prezzo_per_unita": Decimal("2.80")},
            {"nome": "Melanzane", "unita_base": "kg", "prezzo_per_unita": Decimal("3.20")},
            {"nome": "Peperoni", "unita_base": "kg", "prezzo_per_unita": Decimal("3.50")},
            
            # Condimenti
            {"nome": "Olio extravergine d'oliva", "unita_base": "l", "prezzo_per_unita": Decimal("12.00")},
            {"nome": "Sale", "unita_base": "kg", "prezzo_per_unita": Decimal("0.80")},
            {"nome": "Pepe nero", "unita_base": "g", "prezzo_per_unita": Decimal("0.03")},
            {"nome": "Peperoncino", "unita_base": "g", "prezzo_per_unita": Decimal("0.05")},
            
            # Dolci
            {"nome": "Zucchero", "unita_base": "kg", "prezzo_per_unita": Decimal("1.50")},
            {"nome": "Burro", "unita_base": "kg", "prezzo_per_unita": Decimal("8.00")},
            {"nome": "Mascarpone", "unita_base": "kg", "prezzo_per_unita": Decimal("12.00")},
            {"nome": "Caffè", "unita_base": "l", "prezzo_per_unita": Decimal("0.15")},
            {"nome": "Savoiardi", "unita_base": "kg", "prezzo_per_unita": Decimal("8.00")},
            {"nome": "Cacao amaro", "unita_base": "g", "prezzo_per_unita": Decimal("0.02")},
        ]
        
        ingredienti = {}
        for ing_data in ingredienti_data:
            existing = db.query(Ingredient).filter(
                Ingredient.nome == ing_data["nome"],
                Ingredient.unita_base == ing_data["unita_base"]
            ).first()
            
            if not existing:
                ingrediente = Ingredient(**ing_data)
                db.add(ingrediente)
                db.flush()
                ingredienti[ing_data["nome"]] = ingrediente
                print(f"  ✓ Ingrediente: {ing_data['nome']} ({ing_data['unita_base']})")
            else:
                ingredienti[ing_data["nome"]] = existing
                print(f"  → Ingrediente esistente: {ing_data['nome']}")
        
        db.commit()
        
        # 3. VINI
        print("\n🍷 Creazione vini...")
        vini_data = [
            {"nome": "Chianti Classico DOCG", "tipo": "Rosso", "nazione": "Italia", "regione": "Toscana", "prezzo": Decimal("18.50")},
            {"nome": "Brunello di Montalcino", "tipo": "Rosso", "nazione": "Italia", "regione": "Toscana", "prezzo": Decimal("45.00")},
            {"nome": "Barolo DOCG", "tipo": "Rosso", "nazione": "Italia", "regione": "Piemonte", "prezzo": Decimal("38.00")},
            {"nome": "Amarone della Valpolicella", "tipo": "Rosso", "nazione": "Italia", "regione": "Veneto", "prezzo": Decimal("42.00")},
            {"nome": "Pinot Grigio DOC", "tipo": "Bianco", "nazione": "Italia", "regione": "Friuli", "prezzo": Decimal("12.00")},
            {"nome": "Vermentino di Sardegna", "tipo": "Bianco", "nazione": "Italia", "regione": "Sardegna", "prezzo": Decimal("14.00")},
            {"nome": "Gavi DOCG", "tipo": "Bianco", "nazione": "Italia", "regione": "Piemonte", "prezzo": Decimal("16.00")},
            {"nome": "Prosecco Valdobbiadene", "tipo": "Spumante", "nazione": "Italia", "regione": "Veneto", "prezzo": Decimal("15.00")},
            {"nome": "Franciacorta DOCG", "tipo": "Spumante", "nazione": "Italia", "regione": "Lombardia", "prezzo": Decimal("28.00")},
        ]
        
        vini = {}
        for v_data in vini_data:
            existing = db.query(Wine).filter(Wine.nome == v_data["nome"]).first()
            if not existing:
                vino = Wine(**v_data)
                db.add(vino)
                db.flush()
                vini[v_data["nome"]] = vino
                print(f"  ✓ Vino: {v_data['nome']} - €{v_data['prezzo']}")
            else:
                vini[v_data["nome"]] = existing
                print(f"  → Vino esistente: {v_data['nome']}")
        
        db.commit()
        
        # 4. RICETTE
        print("\n🍝 Creazione ricette...")
        ricette_data = [
            {
                "titolo": "Spaghetti alla Carbonara",
                "descrizione": "Piatto romano classico con guanciale croccante, uova cremose e pecorino. La vera carbonara non prevede panna.",
                "porzioni_default": 4,
                "tempo_preparazione": 25,
                "difficolta": "Facile",
                "generi": ["Primi Piatti"],
                "ingredienti": [
                    {"nome": "Spaghetti", "quantita": Decimal("0.100"), "unita": "kg"},
                    {"nome": "Guanciale", "quantita": Decimal("0.030"), "unita": "kg"},
                    {"nome": "Uova", "quantita": Decimal("1.000"), "unita": "pz"},
                    {"nome": "Pecorino Romano", "quantita": Decimal("0.025"), "unita": "kg"},
                    {"nome": "Pepe nero", "quantita": Decimal("1.500"), "unita": "g"},
                ],
                "vini": ["Chianti Classico DOCG"],
                "immagine": "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=800"
            },
            {
                "titolo": "Risotto allo Zafferano",
                "descrizione": "Il celebre risotto milanese con il suo caratteristico colore dorato dato dallo zafferano. Richiede mantecatura attenta.",
                "porzioni_default": 4,
                "tempo_preparazione": 35,
                "difficolta": "Media",
                "generi": ["Primi Piatti"],
                "ingredienti": [
                    {"nome": "Riso Carnaroli", "quantita": Decimal("0.080"), "unita": "kg"},
                    {"nome": "Cipolla", "quantita": Decimal("0.030"), "unita": "kg"},
                    {"nome": "Burro", "quantita": Decimal("0.025"), "unita": "kg"},
                    {"nome": "Parmigiano Reggiano", "quantita": Decimal("0.020"), "unita": "kg"},
                    {"nome": "Olio extravergine d'oliva", "quantita": Decimal("0.010"), "unita": "l"},
                ],
                "vini": ["Pinot Grigio DOC"],
                "immagine": "https://images.unsplash.com/photo-1476124369491-c4443827d7b8?w=800"
            },
            {
                "titolo": "Penne all'Arrabbiata",
                "descrizione": "Pasta al pomodoro piccante, un classico della tradizione romana. Il peperoncino conferisce il caratteristico sapore deciso.",
                "porzioni_default": 4,
                "tempo_preparazione": 20,
                "difficolta": "Facile",
                "generi": ["Primi Piatti"],
                "ingredienti": [
                    {"nome": "Penne rigate", "quantita": Decimal("0.100"), "unita": "kg"},
                    {"nome": "Pomodori pelati", "quantita": Decimal("0.200"), "unita": "kg"},
                    {"nome": "Aglio", "quantita": Decimal("8.000"), "unita": "g"},
                    {"nome": "Peperoncino", "quantita": Decimal("3.000"), "unita": "g"},
                    {"nome": "Olio extravergine d'oliva", "quantita": Decimal("0.020"), "unita": "l"},
                    {"nome": "Basilico fresco", "quantita": Decimal("5.000"), "unita": "g"},
                ],
                "vini": ["Chianti Classico DOCG"],
                "immagine": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=800"
            },
            {
                "titolo": "Tiramisù",
                "descrizione": "Dolce al cucchiaio veneto con strati di savoiardi, caffè e crema al mascarpone. Da servire freddo dopo alcune ore di riposo.",
                "porzioni_default": 8,
                "tempo_preparazione": 30,
                "difficolta": "Media",
                "generi": ["Dolci"],
                "ingredienti": [
                    {"nome": "Mascarpone", "quantita": Decimal("0.063"), "unita": "kg"},
                    {"nome": "Uova", "quantita": Decimal("0.750"), "unita": "pz"},
                    {"nome": "Zucchero", "quantita": Decimal("0.015"), "unita": "kg"},
                    {"nome": "Savoiardi", "quantita": Decimal("0.030"), "unita": "kg"},
                    {"nome": "Caffè", "quantita": Decimal("0.050"), "unita": "l"},
                    {"nome": "Cacao amaro", "quantita": Decimal("5.000"), "unita": "g"},
                ],
                "vini": ["Prosecco Valdobbiadene"],
                "immagine": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=800"
            },
            {
                "titolo": "Pasta alla Norma",
                "descrizione": "Ricetta siciliana con melanzane fritte, salsa di pomodoro e ricotta salata. Un piatto ricco di sapori mediterranei.",
                "porzioni_default": 4,
                "tempo_preparazione": 40,
                "difficolta": "Media",
                "generi": ["Primi Piatti"],
                "ingredienti": [
                    {"nome": "Penne rigate", "quantita": Decimal("0.100"), "unita": "kg"},
                    {"nome": "Melanzane", "quantita": Decimal("0.200"), "unita": "kg"},
                    {"nome": "Pomodorini", "quantita": Decimal("0.150"), "unita": "kg"},
                    {"nome": "Basilico fresco", "quantita": Decimal("10.000"), "unita": "g"},
                    {"nome": "Aglio", "quantita": Decimal("5.000"), "unita": "g"},
                    {"nome": "Olio extravergine d'oliva", "quantita": Decimal("0.050"), "unita": "l"},
                ],
                "vini": ["Vermentino di Sardegna"],
                "immagine": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800"
            },
            {
                "titolo": "Tagliata di Manzo",
                "descrizione": "Filetto di manzo cotto al sangue, tagliato a fette e servito con rucola e scaglie di parmigiano. Piatto elegante e veloce.",
                "porzioni_default": 4,
                "tempo_preparazione": 15,
                "difficolta": "Facile",
                "generi": ["Secondi Piatti"],
                "ingredienti": [
                    {"nome": "Filetto di manzo", "quantita": Decimal("0.200"), "unita": "kg"},
                    {"nome": "Parmigiano Reggiano", "quantita": Decimal("0.015"), "unita": "kg"},
                    {"nome": "Olio extravergine d'oliva", "quantita": Decimal("0.010"), "unita": "l"},
                    {"nome": "Sale", "quantita": Decimal("3.000"), "unita": "g"},
                    {"nome": "Pepe nero", "quantita": Decimal("2.000"), "unita": "g"},
                ],
                "vini": ["Barolo DOCG"],
                "immagine": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800"
            },
        ]
        
        for r_data in ricette_data:
            existing = db.query(Recipe).filter(Recipe.titolo == r_data["titolo"]).first()
            if existing:
                print(f"  → Ricetta esistente: {r_data['titolo']}")
                continue
            
            # Crea ricetta
            ricetta = Recipe(
                titolo=r_data["titolo"],
                descrizione=r_data["descrizione"],
                porzioni_default=r_data["porzioni_default"],
                tempo_preparazione_min=r_data["tempo_preparazione"],
                difficolta=r_data["difficolta"].lower(),
            )
            db.add(ricetta)
            db.flush()
            
            # Aggiungi generi usando la relazione many-to-many
            for genere_nome in r_data["generi"]:
                if genere_nome in generi:
                    ricetta.generi.append(generi[genere_nome])
            
            # Aggiungi ingredienti
            for ing in r_data["ingredienti"]:
                if ing["nome"] in ingredienti:
                    ricetta_ing = RecipeIngredient(
                        ID_RICETTA=ricetta.ID,
                        ID_INGREDIENTE=ingredienti[ing["nome"]].ID,
                        quantita_per_persona=ing["quantita"],
                        unita_misura=ing["unita"],
                    )
                    db.add(ricetta_ing)
            
            # Aggiungi vini
            for vino_nome in r_data["vini"]:
                if vino_nome in vini:
                    ricetta_vino = RecipeWine(
                        ID_RICETTA=ricetta.ID,
                        ID_VINO=vini[vino_nome].ID,
                    )
                    db.add(ricetta_vino)
            
            # Aggiungi immagine
            if r_data.get("immagine"):
                media = Media(
                    ID_RICETTA=ricetta.ID,
                    tipo="immagine",
                    url=r_data["immagine"],
                )
                db.add(media)
            
            db.flush()
            print(f"  ✓ Ricetta: {r_data['titolo']} ({r_data['tempo_preparazione']} min)")
        
        db.commit()
        
        print("\n✅ Popolamento database completato con successo!")
        print(f"   • {len(generi)} generi")
        print(f"   • {len(ingredienti)} ingredienti")
        print(f"   • {len(vini)} vini")
        print(f"   • {len(ricette_data)} ricette")
        
    except Exception as e:
        print(f"\n❌ Errore durante il popolamento: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_database()
