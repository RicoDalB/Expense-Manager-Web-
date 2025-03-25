from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse  #  Importa gli schema

router = APIRouter(prefix="/categories")  #  Prefisso per evitare ripetizioni

# Dipendenza per ottenere la sessione del database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Creare una nuova categoria
@router.post("/", response_model=CategoryResponse)  
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Categoria già esistente.")
    
    base_url = "http://127.0.0.1:8000/static/icons/"
    icon_filename = f"{category.icon}" if category.icon else "default.png"  # Usa default se non viene fornita un'icona
    icon_path = f"{base_url}{icon_filename}"  


    new_category = Category(name=category.name, icon=icon_path)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# 2. Ottenere tutte le categorie
@router.get("/", response_model=list[CategoryResponse])  
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


# 3. Ottenere una categoria specifica
@router.get("/{category_id}", response_model=CategoryResponse)  
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria non trovata.")
    return category


# 4. Modificare una categoria
@router.put("/{category_name}", response_model=CategoryResponse) 
def update_category(category_name: str, updated_category: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria non trovata.")

    category.name = updated_category.name
    db.commit()
    db.refresh(category)
    return category


# 5. Eliminare una categoria
@router.delete("/{category_name}")  
def delete_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria non trovata.")
    
    db.delete(category)
    db.commit()
    return {"message": "Categoria eliminata con successo."}
