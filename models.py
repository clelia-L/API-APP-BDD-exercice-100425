from pydantic import BaseModel

class ProduitBase(BaseModel):
    nom: str
    prix: float

class ProduitCreate(ProduitBase):
    pass

class Produit(ProduitBase):
    id: int

    class Config:
        from_attributes = True
