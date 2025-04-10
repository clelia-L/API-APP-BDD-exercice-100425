from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuration spécifique pour Laragon
db_config = {
    'host': 'localhost',
    'port': 3309,  # Port spécifique de Laragon
    'user': 'root',
    'password': '',  # Mot de passe vide par défaut dans Laragon
    'database': 'magasin_meubles'
}

@app.before_request
def connect_db():
    try:
        g.conn = mysql.connector.connect(**db_config)
        g.cursor = g.conn.cursor(dictionary=True)
    except Error as e:
        return jsonify({"error": str(e)}), 500

@app.teardown_request
def disconnect_db(exception=None):
    if hasattr(g, 'conn') and g.conn.is_connected():
        g.cursor.close()
        g.conn.close()

@app.route('/api/produits', methods=['GET'])
def get_produits():
    try:
        g.cursor.execute("SELECT * FROM produits")
        return jsonify(g.cursor.fetchall())
    except Error as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/produits', methods=['POST'])
def add_produit():
    data = request.get_json()
    if not data or 'nom' not in data or 'prix' not in data:
        return jsonify({"error": "Données manquantes"}), 400

    try:
        g.cursor.execute(
            "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s)",
            (data['nom'], data['prix'], data.get('stock', 0))
        )
        g.conn.commit()
        return jsonify({"id": g.cursor.lastrowid, **data}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
