from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from app.database import SessionLocal
from app.models.expense import Expense
from app.models.category import Category

router = APIRouter()

# DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔮 1. Previsione spesa mensile
@router.get("/expenses/predict-monthly")
def predict_monthly_expense(db: Session = Depends(get_db)):
    today = datetime.today()
    first_day = today.replace(day=1)

    expenses = db.query(Expense).filter(Expense.date >= first_day).all()
    total_spent = sum(exp.amount for exp in expenses)

    days_passed = today.day
    days_in_month = (first_day.replace(month=(first_day.month % 12 + 1), day=1) - timedelta(days=1)).day

    predicted = (total_spent / days_passed) * days_in_month if total_spent > 0 else 0

    return {
        "month": today.strftime("%Y-%m"),
        "total_spent": round(total_spent, 2),
        "predicted_expense": round(predicted, 2)
    }

# 🔁 2. Inserisci spesa ricorrente
@router.post("/expenses/recurring")
def add_recurring_expense(
    description: str,
    amount: float,
    category_id: int,
    interval: str,
    db: Session = Depends(get_db)
):
    valid_intervals = {"daily": 1, "weekly": 7, "monthly": "monthly"}
    if interval not in valid_intervals:
        raise HTTPException(status_code=400, detail="Intervallo non valido: usa 'daily', 'weekly' o 'monthly'.")

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Categoria non valida.")

    today = datetime.today()
    occurrences = []

    for i in range(12):  # 12 occorrenze per l'anno
        if valid_intervals[interval] == "monthly":
            future_date = today + relativedelta(months=i)
        else:
            future_date = today + timedelta(days=valid_intervals[interval] * i)

        db.add(Expense(
            description=description,
            amount=amount,
            date=future_date,
            category_id=category_id
        ))
        occurrences.append(future_date.strftime("%Y-%m-%d"))

    db.commit()
    return {
        "message": f"Spesa ricorrente '{description}' aggiunta con successo.",
        "next_occurrences": occurrences
    }
