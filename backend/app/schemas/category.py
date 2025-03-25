from typing import Optional

from pydantic import BaseModel
#rappresenta il fomrato dei dati accettati e restituiti da api per category

# Schema per la creazione di una categoria
class CategoryCreate(BaseModel):
    name: str
    icon: str

# Schema per l'aggiornamento di una categoria
class CategoryUpdate(BaseModel):
    name: str
    icon: str

# Schema per la risposta della categoria
class CategoryResponse(BaseModel):
    id: int
    name: str
    icon: Optional [str]

    class Config:
        from_attributes = True
