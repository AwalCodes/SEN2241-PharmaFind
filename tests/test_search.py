from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_home_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Pharma-Find API"


def test_search_paracetamol():
    response = client.get("/api/medications/search", params={"name": "Paracetamol"})
    assert response.status_code == 200
    data = response.json()
    assert data["search"] == "Paracetamol"
    assert len(data["results"]) >= 1


def test_search_not_found():
    response = client.get("/api/medications/search", params={"name": "UnknownMed"})
    assert response.status_code == 200
    data = response.json()
    assert data["results"] == []
