import os
# 

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./expences.db")  # Carica il database da variabile d'ambiente, con un valore predefinito
    DEBUG = os.getenv("DEBUG", True)  # Legge il valore di DEBUG da .env o usa True di default

settings = Settings()


