from app.database import SessionLocal
from app.models.category import Category

def run():
    db = SessionLocal()

    #svuota 
    db.query(Category).delete()
    db.commit()

    #categorie da inserire 
    base_url = "http://127.0.0.1:8000/static/icons/"
    categories = [
        {"name": "Affitto", "icon": "\app\icons\affitto.png"},
        {"name": "Assicurazione", "icon": "\app\icons\assicurazione.png"},

    ]
    

    db.commit()
    db.close()
    print("✅ Categorie popolato con successo.")