import sqlite3
import os

# Percorso del database
DATABASE = 'users.db'

def init_db():
    if os.path.exists(DATABASE):
        print(f"Il file {DATABASE} esiste già. Vuoi sovrascriverlo? (s/n)")
        risposta = input().lower()
        if risposta != 's':
            print("Operazione annullata.")
            return

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  registration_date TEXT NOT NULL,
                  last_login TEXT,
                  login_count INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()
    print(f"Database {DATABASE} creato con successo.")

if __name__ == '__main__':
    init_db()