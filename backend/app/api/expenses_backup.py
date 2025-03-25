from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.database import SessionLocal
from app.models.expense import Expense
from app.models.category import Category
from app.schemas.expense import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/expenses")

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Serializzazione categoria sicura
def serialize_category(cat):
    return {
        "id": cat.id,
        "name": cat.name,
        "icon": cat.icon or "default.png"
    } if cat else {
        "id": 0,
        "name": "Sconosciuta",
        "icon": "default.png"
    }

# 1. Creazione spesa
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
        category=serialize_category(category)
    )

# 2. Recupera tutte le spese
@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).options(joinedload(Expense.category)).all()

    return [
        ExpenseResponse(
            id=exp.id,
            description=exp.description,
            amount=exp.amount,
            date=exp.date.strftime("%Y-%m-%d"),
            category=serialize_category(exp.category)
        )
        for exp in expenses
    ]

# 3. Recupera spesa specifica
@router.get("/{id}", response_model=ExpenseResponse)
def get_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).options(joinedload(Expense.category)).filter(Expense.id == id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Spesa non trovata")

    return ExpenseResponse(
        id=expense.id,
        description=expense.description,
        amount=expense.amount,
        date=expense.date.strftime("%Y-%m-%d"),
        category=serialize_category(expense.category)
    )

# 4. Aggiorna spesa
@router.put("/{id}", response_model=ExpenseResponse)
def update_expense(id: int, updated_expense: ExpenseCreate, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Spesa non trovata")

    category = db.query(Category).filter(Category.id == updated_expense.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Categoria non valida.")

    for key, value in updated_expense.model_dump().items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)

    return ExpenseResponse(
        id=expense.id,
        description=expense.description,
        amount=expense.amount,
        date=expense.date.strftime("%Y-%m-%d"),
        category=serialize_category(category)
    )

# 5. Elimina spesa
@router.delete("/{id}")
def delete_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Spesa non trovata")

    db.delete(expense)
    db.commit()
    return {"message": "Spesa eliminata con successo"}

# 6. Categorie più utilizzate
@router.get("/popular-categories/")
def get_popular_categories(db: Session = Depends(get_db), limit: int = 5):
    category_counts = (
        db.query(Expense.category_id, Category.name, func.count(Expense.category_id).label("count"))
        .join(Category, Expense.category_id == Category.id)
        .group_by(Expense.category_id, Category.name)
        .order_by(func.count(Expense.category_id).desc())
        .limit(limit)
        .all()
    )

    return [
        {"category": {"id": cat_id, "name": cat_name}, "count": count}
        for cat_id, cat_name, count in category_counts
    ]
