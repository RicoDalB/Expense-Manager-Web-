from fastapi import APIRouter, Depends, HTTPException
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.expense import Expense
from app.models.category import Category  # Importiamo il modello Category

router = APIRouter()

#  Dependency per ottenere la sessione del database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  1. Predice la spesa totale prevista per il mese corrente
@router.get("/expenses/predict-monthly")
def predict_monthly_expense(db: Session = Depends(get_db)):
    today = datetime.today()
    first_day_of_month = today.replace(day=1)

    # Prendiamo tutte le spese fatte da inizio mese
    expenses = db.query(Expense).filter(Expense.date >= first_day_of_month).all()
    total_spent = sum(exp.amount for exp in expenses)

    days_passed = max(today.day, 1)  # Evitiamo la divisione per 0
    days_in_month = (first_day_of_month.replace(month=(first_day_of_month.month % 12 + 1), day=1) - timedelta(days=1)).day

    # 🔹 Previsione calcolata con media giornaliera attuale
    predicted_expense = (total_spent / days_passed) * days_in_month if total_spent > 0 else 0

    return {
        "month": today.strftime("%Y-%m"),
        "total_spent": total_spent,
        "predicted_expense": round(predicted_expense, 2)  # Arrotondiamo a 2 decimali
    }


#  2. Aggiungere una spesa ricorrente (ora usa `category_id`)
@router.post("/expenses/recurring")
def add_recurring_expense(description: str, amount: float, category_id: int, interval: str, db: Session = Depends(get_db)):
    valid_intervals = {"daily": 1, "weekly": 7, "monthly": "monthly"}

    if interval not in valid_intervals:
        raise HTTPException(status_code=400, detail="L'intervallo deve essere 'daily', 'weekly' o 'monthly'.")

    # Verifica che la categoria esista nel database
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Categoria non valida.")

    today = datetime.today()
    recurrence_type = valid_intervals[interval]
    occurrences = []

    # Creiamo le occorrenze per un anno (12 mesi)
    for i in range(12):
        if recurrence_type == "monthly":
            # 🔹 Se è mensile, calcoliamo la data del mese successivo mantenendo il giorno originale
            future_date = today + relativedelta(month=i)
        else:
            # 🔹 Se è giornaliero o settimanale, aggiungiamo il numero di giorni corrispondente
            future_date = today + timedelta(days=recurrence_type * i)

        recurring_expense = Expense(
            description=description,
            amount=amount,
            date=future_date,
            category_id=category_id
        )
        db.add(recurring_expense)
        occurrences.append(future_date.strftime("%Y-%m-%d"))

    db.commit()
    return {"message": f"Spesa ricorrente '{description}' aggiunta con successo!", "next_occurrences": occurrences}
