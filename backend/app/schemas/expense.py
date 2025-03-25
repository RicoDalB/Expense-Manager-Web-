from pydantic import BaseModel
from datetime import date
from app.schemas.category import CategoryResponse  # Importiamo lo schema della categoria
#rappresenta il fomrato dei dati accettati e restituiti da api per spesa (expense)

# Modello di input per creare una nuova spesa
class ExpenseCreate(BaseModel):
    description: str
    amount: float
    date: date
    category_id: int  # 🔹 Ora usiamo un ID invece di una stringa

# Modello di output per restituire una spesa
class ExpenseResponse(BaseModel):
    id: int  # ID univoco della spesa
    description: str
    amount: float
    date: date
    category: CategoryResponse  # 🔹 Qui restituiamo un oggetto CategoryResponse, non solo un ID

    class Config:
        from_attributes = True  # Compatibilità con SQLAlchemy
