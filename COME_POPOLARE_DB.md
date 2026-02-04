# 🍝 Come Popolare il Database

## Script di Popolazione

Il file `backend/populate_db.py` popola automaticamente il database con dati di esempio.

## Contenuto del Database Dopo il Popolamento

### 👥 Utenti di Test (3)
Tutti con password: `password123`

1. **Mario Rossi**
   - Email: `mario.rossi@example.com`
   - Telefono: 3331234567
   - Indirizzo: Via Roma 1, 20100 Milano

2. **Laura Bianchi**
   - Email: `laura.bianchi@example.com`
   - Telefono: 3339876543
   - Indirizzo: Corso Italia 45, 00100 Roma

3. **Giuseppe Verdi**
   - Email: `giuseppe.verdi@example.com`
   - Telefono: 3335551234
   - Indirizzo: Piazza Duomo 10, 50100 Firenze

### 📚 Generi (8)
- Primi Piatti
- Secondi Piatti
- Antipasti
- Dolci
- Contorni
- Pizze e Focacce
- Salse e Condimenti
- Zuppe e Minestre

### 🥬 Ingredienti (~30)
Con unità di misura e prezzi realistici:
- **Pasta e Cereali**: Spaghetti (kg), Penne (kg), Riso Carnaroli (kg), Farina (kg)
- **Proteine**: Guanciale (kg), Pancetta (kg), Parmigiano (kg), Pecorino (kg), Mozzarella (kg), Uova (pz), Filetto (kg)
- **Verdure**: Pomodori pelati (kg), Pomodorini (kg), Basilico (g), Aglio (g), Cipolla (kg), Zucchine (kg), Melanzane (kg), Peperoni (kg)
- **Condimenti**: Olio EVO (l), Sale (kg), Pepe (g), Peperoncino (g)
- **Dolci**: Zucchero (kg), Burro (kg), Mascarpone (kg), Caffè (l), Savoiardi (kg), Cacao (g)

### 🍷 Vini (9)
Con prezzi realistici:
- **Rossi**: Chianti Classico (€18.50), Brunello (€45.00), Barolo (€38.00), Amarone (€42.00)
- **Bianchi**: Pinot Grigio (€12.00), Vermentino (€14.00), Gavi (€16.00)
- **Spumanti**: Prosecco (€15.00), Franciacorta (€28.00)

### 🍝 Ricette (6 complete)

#### 1. Spaghetti alla Carbonara
- **Tempo**: 25 min | **Difficoltà**: Facile
- **Ingredienti**: Spaghetti, Guanciale, Uova, Pecorino, Pepe
- **Vino**: Chianti Classico DOCG

#### 2. Risotto allo Zafferano
- **Tempo**: 35 min | **Difficoltà**: Media
- **Ingredienti**: Riso Carnaroli, Cipolla, Burro, Parmigiano, Olio
- **Vino**: Pinot Grigio DOC

#### 3. Penne all'Arrabbiata
- **Tempo**: 20 min | **Difficoltà**: Facile
- **Ingredienti**: Penne, Pomodori pelati, Aglio, Peperoncino, Olio, Basilico
- **Vino**: Chianti Classico DOCG

#### 4. Tiramisù
- **Tempo**: 30 min | **Difficoltà**: Media
- **Ingredienti**: Mascarpone, Uova, Zucchero, Savoiardi, Caffè, Cacao
- **Vino**: Prosecco Valdobbiadene

#### 5. Pasta alla Norma
- **Tempo**: 40 min | **Difficoltà**: Media
- **Ingredienti**: Penne, Melanzane, Pomodorini, Basilico, Aglio, Olio
- **Vino**: Vermentino di Sardegna

#### 6. Tagliata di Manzo
- **Tempo**: 15 min | **Difficoltà**: Facile
- **Ingredienti**: Filetto di manzo, Parmigiano, Olio, Sale, Pepe
- **Vino**: Barolo DOCG

---

## Come Eseguire lo Script

### Opzione 1: Da PowerShell
```powershell
cd backend
python populate_db.py
```

### Opzione 2: Con ambiente virtuale attivo
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python populate_db.py
```

## Output Atteso

```
🍝 Inizio popolamento database Cucina Italiana...

👥 Creazione utenti di test...
  ✓ Utente: Mario Rossi (mario.rossi@example.com)
  ✓ Utente: Laura Bianchi (laura.bianchi@example.com)
  ✓ Utente: Giuseppe Verdi (giuseppe.verdi@example.com)

📚 Creazione generi...
  ✓ Genere: Primi Piatti
  ✓ Genere: Secondi Piatti
  ...

🥬 Creazione ingredienti...
  ✓ Ingrediente: Spaghetti (kg)
  ✓ Ingrediente: Guanciale (kg)
  ...

🍷 Creazione vini...
  ✓ Vino: Chianti Classico DOCG - €18.50
  ...

🍝 Creazione ricette...
  ✓ Ricetta: Spaghetti alla Carbonara (25 min)
  ...

✅ Popolamento database completato con successo!
   • 8 generi
   • 30 ingredienti
   • 9 vini
   • 6 ricette
```

## Note Importanti

⚠️ **Lo script NON elimina i dati esistenti** - verifica sempre l'esistenza prima di inserire

✅ **Gestione errori** - se un elemento esiste già, viene saltato senza errore

🔄 **Riesecuzione sicura** - puoi eseguire lo script più volte senza duplicazioni

## Credenziali di Test

Dopo il popolamento, puoi accedere al frontend con:

- **Email**: mario.rossi@example.com
- **Password**: password123

Oppure con gli altri 2 utenti usando le email corrispondenti.

## Verificare il Popolamento

Puoi verificare che i dati siano stati inseriti correttamente:

1. Avvia il backend: `cd backend; .\start.ps1`
2. Apri il browser su: http://localhost:8000/docs
3. Testa gli endpoint:
   - `GET /api/recipes` - Lista ricette
   - `GET /api/recipes/genres` - Lista generi
   - `POST /api/auth/login` - Login con credenziali test

## Aggiungi Colonna Prezzo ai Vini

Se la tabella VINI non ha la colonna `prezzo`, esegui prima:

```sql
ALTER TABLE VINI ADD COLUMN prezzo DECIMAL(10,2) NULL;
```

Oppure usa lo script: `add_wine_price.sql`
