from app.database import Base, engine
from app.models.expense import Expense  # Import esplicito del modello
from app.models.category import Category

print("Creazione del database...")
Base.metadata.create_all(engine)  # Forza la creazione delle tabelle
print("Database creato con successo!")
