from fastapi import FastAPI
import logging
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

# Configuration des logs pour le débogage
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Gestionnaire d'erreurs global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erreur non capturée : {exc}", exc_info=True)
    return {"detail": "Erreur interne du serveur"}

# Vérification du démarrage
@app.on_event("startup")
async def startup_db():
    try:
        # Testez votre connexion MySQL ici si nécessaire
        logger.info("✅ Démarrage réussi")
    except Exception as e:
        logger.critical(f"❌ Échec du démarrage : {e}", exc_info=True)
        raise  # Arrête l'application si critique

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

from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Équivalent de @app.on_event("startup")
    try:
        logger.info("✅ Initialisation de la base de données...")
        # Ici : votre logique de connexion MySQL
        yield
    except Exception as e:
        logger.critical(f"❌ Échec du démarrage : {e}")
        raise
    finally:
        # Équivalent de @app.on_event("shutdown")
        logger.info("🔌 Nettoyage des ressources...")

app = FastAPI(lifespan=lifespan)

# Vos routes restent inchangées
@app.get("/")
async def root():
    return {"message": "Hello World"}
