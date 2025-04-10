from database import get_db_connection

def get_produits():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produit")
    produits = cursor.fetchall()
    conn.close()
    return produits

def create_produit(nom: str, prix: float):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produit (nom, prix) VALUES (%s, %s)", (nom, prix))
    conn.commit()
    produit_id = cursor.lastrowid
    conn.close()
    return produit_id

def delete_produit(produit_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produit WHERE id = %s", (produit_id,))
    conn.commit()
    conn.close()

def update_produit(produit_id: int, new_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE produit SET id = %s WHERE id = %s", (new_id, produit_id))
    conn.commit()
    conn.close()
