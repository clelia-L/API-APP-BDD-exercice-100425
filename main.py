from fastapi import FastAPI, HTTPException
from models import Produit, ProduitCreate
from crud import get_produits, create_produit, delete_produit, update_produit
from database import init_db

app = FastAPI()

# Initialiser la base de données au démarrage
@app.on_event("startup")
def on_startup():
    init_db()

# Endpoints CRUD
@app.get("/produits/", response_model=list[Produit])
def lire_produits():
    return get_produits()

@app.post("/produits/", response_model=Produit)
def ajouter_produit(produit: ProduitCreate):
    produit_id = create_produit(produit.nom, produit.prix)
    return {**produit.dict(), "id": produit_id}

@app.delete("/produits/{produit_id}")
def supprimer_produit(produit_id: int):
    delete_produit(produit_id)
    return {"message": "Produit supprimé"}

@app.put("/produits/{produit_id}")
def modifier_id_produit(produit_id: int, new_id: int):
    update_produit(produit_id, new_id)
    return {"message": "ID mis à jour"}
