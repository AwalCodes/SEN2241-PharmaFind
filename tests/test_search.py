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


def test_pharmacist_login_success():
    response = client.post(
        "/api/pharmacist/login",
        json={"username": "pharmacist", "password": "pharma123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "Pharmacist"
    assert "token" in data


def test_add_pharmacy_success():
    login_response = client.post(
        "/api/pharmacist/login",
        json={"username": "pharmacist", "password": "pharma123"},
    )
    token = login_response.json()["token"]

    response = client.post(
        "/api/pharmacies",
        json={
            "pharmacy_name": "CommunityCare Pharmacy",
            "address": "99 Test Avenue",
            "medication_name": "Vitamin C",
            "quantity": 15,
        },
        headers={"X-Pharmacist-Token": token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Pharmacy added"
    assert data["pharmacy_name"] == "CommunityCare Pharmacy"


def test_get_pharmacy_medications():
    response = client.get("/api/pharmacies/1/medications")
    assert response.status_code == 200
    data = response.json()
    assert data["pharmacy_id"] == 1
    assert len(data["medications"]) >= 1


def test_update_stock_success():
    login_response = client.post(
        "/api/pharmacist/login",
        json={"username": "pharmacist", "password": "pharma123"},
    )
    token = login_response.json()["token"]

    response = client.post(
        "/api/pharmacies/1/stock",
        json={"medication_name": "Paracetamol", "new_quantity": 30},
        headers={"X-Pharmacist-Token": token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Stock updated"
    assert data["new_quantity"] == 30


def test_update_stock_pharmacy_not_found():
    login_response = client.post(
        "/api/pharmacist/login",
        json={"username": "pharmacist", "password": "pharma123"},
    )
    token = login_response.json()["token"]

    response = client.post(
        "/api/pharmacies/999/stock",
        json={"medication_name": "Paracetamol", "new_quantity": 10},
        headers={"X-Pharmacist-Token": token},
    )
    assert response.status_code == 404


def test_update_stock_negative_quantity():
    login_response = client.post(
        "/api/pharmacist/login",
        json={"username": "pharmacist", "password": "pharma123"},
    )
    token = login_response.json()["token"]

    response = client.post(
        "/api/pharmacies/1/stock",
        json={"medication_name": "Paracetamol", "new_quantity": -1},
        headers={"X-Pharmacist-Token": token},
    )
    assert response.status_code == 400


def test_update_stock_requires_login():
    response = client.post(
        "/api/pharmacies/1/stock",
        json={"medication_name": "Paracetamol", "new_quantity": 10},
    )
    assert response.status_code == 401
