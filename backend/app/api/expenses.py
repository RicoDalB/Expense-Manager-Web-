from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.database import SessionLocal
from app.models.expense import Expense
from app.models.category import Category
from app.schemas.expense import ExpenseCreate, ExpenseResponse

router = APIRouter()

# Dipendenza per ottenere la sessione del DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Creazione spesa
@router.post("/expenses/", response_model=ExpenseResponse)
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
        category={
            "id": category.id,
            "name": category.name,
            "icon": category.icon  # ✔️ AGGIUNTO ICON
        }
    )

# 2. Get tutte le spese
@router.get("/expenses/", response_model=list[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).options(joinedload(Expense.category)).all()

    return [
        ExpenseResponse(
            id=exp.id,
            description=exp.description,
            amount=exp.amount,
            date=exp.date.strftime("%Y-%m-%d"),
            category={
                "id": exp.category.id,
                "name": exp.category.name,
                "icon": exp.category.icon or "default.png"
            } if exp.category else {
                "id": 0,
                "name": "Sconosciuta",
                "icon": "default.png"
            }
        )
        for exp in expenses
    ]

# 3. Get spesa specifica
@router.get("/expenses/{id}", response_model=ExpenseResponse)
def get_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).options(joinedload(Expense.category)).filter(Expense.id == id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Spesa non trovata")

    return ExpenseResponse(
        id=expense.id,
        description=expense.description,
        amount=expense.amount,
        date=expense.date.strftime("%Y-%m-%d"),
        category={
            "id": expense.category.id,
            "name": expense.category.name,
            "icon": expense.category.icon  # ✔️ AGGIUNTO ICON
        } if expense.category else None
    )


# 4. Modifica spesa
@router.put("/expenses/{id}", response_model=ExpenseResponse)
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
        category={
            "id": category.id,
            "name": category.name,
            "icon": category.icon  # ✔️ AGGIUNTO ICON
        }
    )


# 5. Elimina spesa
@router.delete("/expenses/{id}")
def delete_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Spesa non trovata")

    db.delete(expense)
    db.commit()
    return {"message": "Spesa eliminata con successo"}

# 6. Categorie più utilizzate
@router.get("/expenses/popular-categories/")
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
