from sqlalchemy import Column, Integer, String, JSON
from app.database import Base  # Assicurati che Base sia importato correttamente
# contiene le definizioni dei modelli di database (SqlAccademy) rappresenta tabella database di category

class Category(Base):  # Il modello deve ereditare da Base
    __tablename__ = "categories"  # Nome corretto della tabella

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, unique=True, nullable=False)  
    color = Column(String, nullable=True)  
    icon =Column (String, nullable= True)
