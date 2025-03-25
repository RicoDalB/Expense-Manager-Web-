from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from collections import defaultdict
from datetime import datetime
from app.database import SessionLocal
from app.models.expense import Expense
from app.models.category import Category

router = APIRouter()

# DB Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Helper per serializzare categoria
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

# 1. Riepilogo spese totali
@router.get("/summary")
def get_summary(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato data non valido (YYYY-MM-DD)")

    expenses = db.query(Expense).options(joinedload(Expense.category)).filter(
        Expense.date.between(start, end)
    ).all()

    total_expenses = sum(exp.amount for exp in expenses)

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_expenses": total_expenses,
        "num_expenses": len(expenses),
        "expenses": [
            {
                "id": exp.id,
                "description": exp.description,
                "amount": exp.amount,
                "date": exp.date.strftime("%Y-%m-%d"),
                "category": serialize_category(exp.category)
            }
            for exp in expenses
        ]
    }

# 2. Spese per categoria
@router.get("/by-category")
def get_expenses_by_category(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato data non valido")

    category_totals = (
        db.query(Category.id, Category.name, func.sum(Expense.amount))
        .join(Expense, Expense.category_id == Category.id)
        .filter(Expense.date.between(start, end))
        .group_by(Category.id, Category.name)
        .all()
    )

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_by_category": [
            {"id": cat_id, "name": cat_name, "total": total}
            for cat_id, cat_name, total in category_totals
        ]
    }

# 3. Trend temporale
@router.get("/trends")
def get_expenses_trends(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato data non valido")

    expenses = db.query(Expense).options(joinedload(Expense.category)).filter(
        Expense.date.between(start, end)
    ).all()

    trends = defaultdict(float)
    for exp in expenses:
        key = exp.date.strftime("%Y-%m-%d")
        trends[key] += exp.amount

    return {
        "start_date": start_date,
        "end_date": end_date,
        "trend_data": [{"date": date, "total_spent": amount} for date, amount in trends.items()],
        "expenses": [
            {
                "id": exp.id,
                "description": exp.description,
                "amount": exp.amount,
                "date": exp.date.strftime("%Y-%m-%d"),
                "category": serialize_category(exp.category)
            }
            for exp in expenses
        ]
    }

# 4. Spese più alte
@router.get("/top-expenses")
def get_top_expenses(start_date: str, end_date: str, limit: int = 5, db: Session = Depends(get_db)):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato data non valido")

    expenses = db.query(Expense).options(joinedload(Expense.category)).filter(
        Expense.date.between(start, end)
    ).order_by(Expense.amount.desc()).limit(limit).all()

    return {
        "start_date": start_date,
        "end_date": end_date,
        "top_expenses": [
            {
                "id": exp.id,
                "description": exp.description,
                "amount": exp.amount,
                "date": exp.date.strftime("%Y-%m-%d"),
                "category": serialize_category(exp.category)
            }
            for exp in expenses
        ]
    }

# 5. Spesa media
@router.get("/average")
def get_average_expense(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato data non valido")

    expenses = db.query(Expense).filter(Expense.date.between(start, end)).all()
    total_expenses = sum(exp.amount for exp in expenses)
    days_count = (end - start).days + 1
    monthly_count = days_count / 30

    return {
        "start_date": start_date,
        "end_date": end_date,
        "average_expense": {
            "daily": total_expenses / days_count if days_count else 0,
            "monthly": total_expenses / monthly_count if monthly_count else 0
        }
    }

# 6. Filtro
@router.get("/filter")
def filter_expenses(
    category_id: int = Query(None, alias="category"),
    min_amount: float = Query(None, alias="min"),
    max_amount: float = Query(None, alias="max"),
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Expense).options(joinedload(Expense.category))

    if category_id:
        query = query.filter(Expense.category_id == category_id)
    if min_amount:
        query = query.filter(Expense.amount >= min_amount)
    if max_amount:
        query = query.filter(Expense.amount <= max_amount)
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Expense.date.between(start, end))
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato data non valido")

    expenses = query.all()

    return {
        "start_date": start_date,
        "end_date": end_date,
        "filtered_expenses": [
            {
                "id": exp.id,
                "description": exp.description,
                "amount": exp.amount,
                "date": exp.date.strftime("%Y-%m-%d"),
                "category": serialize_category(exp.category)
            }
            for exp in expenses
        ]
    }
