from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_home_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Pharma-Find" in response.text


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


def test_get_pharmacies():
    response = client.get("/api/pharmacies")
    assert response.status_code == 200
    data = response.json()
    assert "pharmacies" in data
    assert len(data["pharmacies"]) >= 1


def test_update_stock_success():
    response = client.post(
        "/api/pharmacies/1/stock",
        json={"medication_name": "Paracetamol", "new_quantity": 30},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Stock updated"
    assert data["new_quantity"] == 30


def test_update_stock_pharmacy_not_found():
    response = client.post(
        "/api/pharmacies/999/stock",
        json={"medication_name": "Paracetamol", "new_quantity": 10},
    )
    assert response.status_code == 404


def test_update_stock_negative_quantity():
    response = client.post(
        "/api/pharmacies/1/stock",
        json={"medication_name": "Paracetamol", "new_quantity": -1},
    )
    assert response.status_code == 400
