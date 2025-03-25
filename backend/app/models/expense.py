from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base  # Assicurati che Base sia importato correttamente
from app.models.category import Category
# contiene le definizioni dei modelli di database (SqlAccademy) rappresenta tabella database di expense

class Expense(Base):  # Il modello deve ereditare da Base
    __tablename__ = "expenses"  # Nome corretto della tabella

    id = Column(Integer, primary_key=True, index=True)  # Chiave primaria
    description = Column(String, nullable=False)  # Descrizione della spesa
    amount = Column(Float, nullable=False)  # Importo della spesa
    date = Column(Date, nullable=False)  # Data della spesa
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)  # Categoria della spesa

    #relazione tra tabelle 
    category = relationship("Category")
