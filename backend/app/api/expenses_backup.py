from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app.models.expense import Expense
from app.models.category import Category  # Importiamo il modello Category
from app.schemas.expense import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/expenses")  # ✅ Usa il prefisso per evitare `/expenses/expenses/`

# Dependency per ottenere la sessione del database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Creare una nuova spesa con `category_id`
@router.post("/", response_model=ExpenseResponse)  
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == expense.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Categoria non valida.")

    new_expense = Expense(
        description=expense.description,
        amount=expense.amount,
        date=expense.date,
        category_id=expense.category_id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return ExpenseResponse(
        id=new_expense.id,
        description=new_expense.description,
        amount=new_expense.amount,
        date=new_expense.date.strftime("%Y-%m-%d"),
        category={"id": category.id, "name": category.name}
    )

#  2. Recuperare tutte le spese con il nome della categoria
@router.get("/", response_model=list[ExpenseResponse])  # ✅ Tolto `/expenses/`
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).outerjoin(Category).all()  # ✅ Outerjoin per evitare errori con categorie mancanti
    
    return [
        ExpenseResponse(
            id=exp.id,
            description=exp.description,
            amount=exp.amount,
            date=exp.date.strftime("%Y-%m-%d"),
            category={"id": exp.category.id, "name": exp.category.name} if exp.category else None
        )
        for exp in expenses
    ]

#  3. Recuperare una spesa specifica con nome categoria
@router.get("/{id}", response_model=ExpenseResponse)  # ✅ Tolto `/expenses/`
def get_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).outerjoin(Category).filter(Expense.id == id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Spesa non trovata")
    
    return ExpenseResponse(
        id=expense.id,
        description=expense.description,
        amount=expense.amount,
        date=expense.date.strftime("%Y-%m-%d"),
        category={"id": expense.category.id, "name": expense.category.name} if expense.category else None
    )

#  4. Modificare una spesa (ora aggiorna anche la categoria)
@router.put("/{id}", response_model=ExpenseResponse)  # ✅ Tolto `/expenses/`
def update_expense(id: int, updated_expense: ExpenseCreate, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Spesa non trovata")
    
    if updated_expense.category_id:
        category = db.query(Category).filter(Category.id == updated_expense.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Categoria non valida.")

    # Aggiorna i campi della spesa
    for key, value in updated_expense.model_dump().items():  # ✅ Usa `.dict()` per FastAPI v1
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    
    return ExpenseResponse(
        id=expense.id,
        description=expense.description,
        amount=expense.amount,
        date=expense.date.strftime("%Y-%m-%d"),
        category={"id": expense.category.id, "name": expense.category.name} if expense.category else None
    )

#  5. Eliminare una spesa
@router.delete("/{id}")  # ✅ Tolto `/expenses/`
def delete_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Spesa non trovata")
    
    db.delete(expense)
    db.commit()
    return {"message": "Spesa eliminata con successo"}

#  6. Ottenere le categorie più utilizzate
@router.get("/popular-categories/")  # ✅ Tolto `/expenses/`
def get_popular_categories(db: Session = Depends(get_db), limit: int = 5):
    category_counts = (
        db.query(Expense.category_id, Category.name, func.count(Expense.category_id).label("count"))
        .join(Category, Expense.category_id == Category.id)
        .group_by(Expense.category_id, Category.name)
        .order_by(func.count(Expense.category_id).desc())
        .limit(limit)
        .all()
    )

    return [{"category": {"id": cat_id, "name": cat_name}, "count": count} for cat_id, cat_name, count in category_counts]
