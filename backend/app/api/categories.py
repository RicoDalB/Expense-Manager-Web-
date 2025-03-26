from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories")

# 🔗 Dipendenza DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1️⃣ Crea nuova categoria
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Categoria già esistente.")

     # ✅ Costruisci l'URL completo dell'icona
    base_url = "http://127.0.0.1:8000/icons/"
    icon_name = category.icon or "default"
    if not icon_name.endswith(".png"):
        icon_name += ".png"
    icon_path = f"{base_url}{icon_name}"

    new_cat = Category(name=category.name, icon=icon_path)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)

    return new_cat

# 2️⃣ Ottieni tutte le categorie
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()

    # Aggiungi ".png" all'icona di ogni categoria se non è presente
    for category in categories:
        if not category.icon.endswith(".png"):
            category.icon = f"{category.icon}.png"  # Aggiungi .png

    return categories


# 3️⃣ Ottieni categoria per ID
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria non trovata.")
    return category

# 4️⃣ Aggiorna una categoria (per nome)
@router.put("/{category_name}", response_model=CategoryResponse)
def update_category(category_name: str, updated_category: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria non trovata.")

    category.name = updated_category.name
    db.commit()
    db.refresh(category)
    return category

# 5️⃣ Elimina una categoria (per nome)
@router.delete("/{category_name}")
def delete_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria non trovata.")

    db.delete(category)
    db.commit()
    return {"message": "Categoria eliminata con successo."}
