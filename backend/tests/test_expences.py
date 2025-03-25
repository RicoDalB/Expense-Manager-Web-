from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 📌 1. Test: Creare una nuova categoria per testare le spese
def test_create_category():
    response = client.post("/categories/", json={"name": "Alimentari"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alimentari"
    assert "id" in data  # Controlla che l'ID sia presente

# 📌 2. Test: Creare una spesa valida
def test_create_expense():
    response = client.post("/expenses/", json={
        "description": "Cena fuori",
        "amount": 25.50,
        "date": "2025-02-15",
        "category_id": 1  # Usa la categoria creata prima
    })
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Cena fuori"
    assert data["amount"] == 25.50
    assert data["category"]["id"] == 1  # Controlla che sia associata alla categoria corretta

# 📌 3. Test: Creare una spesa senza un campo obbligatorio (importo mancante)
def test_create_expense_missing_amount():
    response = client.post("/expenses/", json={
        "description": "Cena senza prezzo",
        "date": "2025-02-15",
        "category_id": 1
    })
    assert response.status_code == 422  # 422 significa errore di validazione

# 📌 4. Test: Ottenere tutte le spese
def test_get_expenses():
    response = client.get("/expenses/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Controlla che sia una lista
    assert len(data) > 0  # Controlla che ci sia almeno una spesa

# 📌 5. Test: Ottenere una spesa specifica
def test_get_expense_by_id():
    response = client.get("/expenses/1")  # Assumiamo che l'ID 1 esista
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Cena fuori"

# 📌 6. Test: Modificare una spesa
def test_update_expense():
    response = client.put("/expenses/1", json={
        "description": "Cena aggiornata",
        "amount": 30.00,
        "date": "2025-02-16",
        "category_id": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Cena aggiornata"
    assert data["amount"] == 30.00

# 📌 7. Test: Eliminare una spesa
def test_delete_expense():
    response = client.delete("/expenses/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Spesa eliminata con successo."

# 📌 8. Test: Ottenere una spesa inesistente
def test_get_nonexistent_expense():
    response = client.get("/expenses/9999")  # Un ID inesistente
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Spesa non trovata."
