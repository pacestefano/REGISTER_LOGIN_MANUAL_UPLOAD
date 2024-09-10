from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Aggiungi questa importazione
import sqlite3
import bcrypt
from datetime import datetime
import os
from google.oauth2 import id_token
from google.auth.transport import requests
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://pacestefano.github.io", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})  # Aggiungi questa riga per abilitare CORS

# Percorso del database
DATABASE = 'users.db'

# Inizializzazione del database
def init_db():
    if not os.path.exists(DATABASE):
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
        print("Database creato con successo.")

init_db()

# Funzione per ottenere una connessione al database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Carica il client ID dal file JSON
with open('google_client_secret.json', 'r') as f:
    client_secret = json.load(f)
    CLIENT_ID = client_secret['web']['client_id']

# Funzione per registrare un nuovo utente
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    try:
        conn.execute("INSERT INTO users (email, password, registration_date) VALUES (?, ?, ?)", 
                     (email, hashed_password, registration_date))
        conn.commit()
        return jsonify({"message": "Utente registrato con successo"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email già registrata"}), 400
    finally:
        conn.close()

# Funzione per il login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("UPDATE users SET last_login = ?, login_count = login_count + 1 WHERE id = ?", 
                     (last_login, user['id']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Login effettuato con successo"}), 200
    else:
        conn.close()
        return jsonify({"error": "Credenziali non valide"}), 401

# Rotta per visualizzare la tabella degli utenti
@app.route('/users', methods=['GET'])
def users():
    conn = get_db()
    users = conn.execute("SELECT id, email, registration_date, last_login, login_count FROM users").fetchall()
    conn.close()
    return render_template('users.html', users=users)

# Endpoint per la verifica del token
@app.route('/verify_token', methods=['POST'])
def verify_token():
    token = request.json['token']
    try:
        # Usa il CLIENT_ID caricato dal file
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        return jsonify({"message": "Token valido", "userid": userid}), 200
    except ValueError:
        # Invalid token
        return jsonify({"error": "Token non valido"}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)