from flask import Flask, request, jsonify
from flask_cors import CORS
import google.cloud.logging
import logging

app = Flask(__name__)
CORS(app)

# Configura il logging
client = google.cloud.logging.Client()
client.setup_logging()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Qui dovresti implementare la logica di registrazione
    # Per ora, simuliamo una registrazione riuscita
    logging.info(f"Tentativo di registrazione per l'email: {email}")
    
    return jsonify({"message": f"Registrazione riuscita per {email}"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Qui dovresti implementare la logica di login
    # Per ora, simuliamo un login riuscito
    logging.info(f"Tentativo di login per l'email: {email}")
    
    return jsonify({"message": f"Login riuscito per {email}"}), 200

if __name__ == "__main__":
    app.run(debug=True)