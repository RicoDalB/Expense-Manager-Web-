from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)  # 🔹 Istanza del client per i test
