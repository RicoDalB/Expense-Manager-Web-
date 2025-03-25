from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 📌 1. Test: Creare una nuova categoria
def test_create_category():
    response = client.post("/categories/", json={"name": "Viaggi"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Viaggi"
    assert "id" in data  # Controlla che l'ID sia presente

# 📌 2. Test: Ottenere tutte le categorie
def test_get_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Controlla che sia una lista
    assert len(data) > 0  # Controlla che ci sia almeno una categoria

# 📌 3. Test: Ottenere una categoria specifica
def test_get_category_by_id():
    response = client.get("/categories/1")  # Assumiamo che l'ID 1 esista
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Viaggi"

# 📌 4. Test: Modificare una categoria
def test_update_category():
    response = client.put("/categories/1", json={"name": "Turismo"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Turismo"

# 📌 5. Test: Eliminare una categoria
def test_delete_category():
    response = client.delete("/categories/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Categoria eliminata con successo."

# 📌 6. Test: Ottenere una categoria inesistente
def test_get_nonexistent_category():
    response = client.get("/categories/9999")  # Un ID inesistente
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Categoria non trovata."
