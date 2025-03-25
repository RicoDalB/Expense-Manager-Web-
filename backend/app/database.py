from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
#crea database e sessione database

#gestisce connessione al database
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

#crea sessioni per interagire con il database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#definire modelli di tabelle
Base = declarative_base()

