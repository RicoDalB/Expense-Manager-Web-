from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.api import expenses, expenses_stats, expenses_backup, expenses_ai, categories

app = FastAPI()
icons_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons"))
app.mount("/icons", StaticFiles(directory=icons_path), name="icons")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Permette richieste dal frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permette tutti i metodi (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permette tutti gli headers
)

#inclusione delle api
#app.include_router(expenses.router)
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(expenses_stats.router, prefix="/expenses/stats", tags=["Stats"])
app.include_router(expenses_backup.router, prefix="/expenses/backup", tags=["Backup"])
app.include_router(expenses_ai.router, prefix="/expenses/ai", tags=["AI"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/")
def home():
    return {"message": "Expense Manager API is running!"}

