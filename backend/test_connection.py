"""
Script per testare la connessione al database Aiven
NON crea tabelle - le tabelle devono già esistere su Aiven
"""
import sys
from sqlalchemy import text
from app.db import engine
from app.core.config import settings

def test_connection():
    try:
        print("=" * 60)
        print("Test Connessione Database Aiven - Cucina Italiana")
        print("=" * 60)
        print("")
        
        # Test connessione
        print("🔌 Test connessione al database...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        print("✓ Connessione al database riuscita!")
        
        # Verifica che le tabelle esistano
        print("\n📋 Verifica tabelle esistenti...")
        with engine.connect() as connection:
            # Verifica alcune tabelle principali
            tables_to_check = ['UTENTI', 'RICETTE', 'INGREDIENTI', 'GENERI', 'ORDINI']
            existing_tables = []
            missing_tables = []
            
            for table in tables_to_check:
                result = connection.execute(
                    text(f"SELECT COUNT(*) as cnt FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = '{table}'")
                )
                count = result.fetchone()[0]
                if count > 0:
                    existing_tables.append(table)
                else:
                    missing_tables.append(table)
            
            if existing_tables:
                print(f"\n✓ Tabelle trovate ({len(existing_tables)}):")
                for table in existing_tables:
                    print(f"  - {table}")
            
            if missing_tables:
                print(f"\n⚠ Tabelle mancanti ({len(missing_tables)}):")
                for table in missing_tables:
                    print(f"  - {table}")
                print("\nATTENZIONE: Alcune tabelle non sono presenti nel database!")
                print("Assicurati di aver eseguito lo script SQL di creazione su Aiven.")
            else:
                print("\n✓ Tutte le tabelle principali sono presenti!")
        
        print("\n" + "=" * 60)
        print("✅ Test completato con successo!")
        print("=" * 60)
        print("\nIl database è pronto per l'uso.")
        print("Puoi avviare il server con: uvicorn app.main:app --reload")
        print("")
        
    except Exception as e:
        print(f"\n❌ Errore durante il test del database:")
        print(f"  {str(e)}")
        print("\n📖 Verifica:")
        print("  1. Le credenziali nel file .env sono corrette")
        print("  2. Il database Aiven è attivo e accessibile")
        print("  3. Il tuo IP è nella whitelist di Aiven")
        print("  4. Le tabelle sono state create nel database")
        print("\n📝 DATABASE_URL configurato:")
        # Maschera la password nell'output
        masked_url = settings.database_url
        if '@' in masked_url:
            parts = masked_url.split('@')
            if ':' in parts[0]:
                user_pass = parts[0].split(':')
                masked_url = f"{user_pass[0].split('//')[0]}//{user_pass[0].split('//')[1]}:****@{parts[1]}"
        print(f"  {masked_url}")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()
