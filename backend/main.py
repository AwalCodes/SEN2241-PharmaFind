from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.models import Medication, Pharmacist, Pharmacy

app = FastAPI(
    title="Pharma-Find API",
    description="Simple API to search medication availability in pharmacies.",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StockUpdateRequest(BaseModel):
    medication_name: str
    new_quantity: int


class PharmacistLoginRequest(BaseModel):
    username: str
    password: str


class AddPharmacyRequest(BaseModel):
    pharmacy_name: str
    address: str
    medication_name: str
    quantity: int


# Demo data: 15 pharmacies in Yaounde with common medicines and stock levels.
DEMO_PHARMACIES = [
    ("Pharmacie du Centre", "Avenue Kennedy, Bastos, Yaounde", [
        ("Paracetamol", 80), ("Ibuprofen", 55), ("Amoxicillin", 40), ("Vitamin C", 60), ("Omeprazole", 25),
    ]),
    ("Pharmacie Mokolo", "Marché Mokolo, Yaounde", [
        ("Paracetamol", 120), ("Metronidazole", 35), ("Ciprofloxacin", 28), ("Aspirin", 50), ("Cetirizine", 22),
    ]),
    ("Pharmacie Essos", "Carrefour Essos, Yaounde", [
        ("Paracetamol", 45), ("Ibuprofen", 0), ("Amoxicillin", 30), ("Diclofenac", 18), ("Metformin", 40),
    ]),
    ("Pharmacie Melen", "Rue Melen, Yaounde", [
        ("Paracetamol", 65), ("Artemether-Lumefantrine", 20), ("Chloroquine", 15), ("Vitamin C", 70), ("Amlodipine", 12),
    ]),
    ("Pharmacie Obili", "Quartier Obili, Yaounde", [
        ("Paracetamol", 90), ("Ibuprofen", 42), ("Omeprazole", 30), ("Cetirizine", 35), ("Amoxicillin", 25),
    ]),
    ("Pharmacie Emana", "Boulevard du 20 Mai, Emana, Yaounde", [
        ("Paracetamol", 55), ("Metronidazole", 40), ("Ciprofloxacin", 32), ("Aspirin", 28), ("Vitamin C", 45),
    ]),
    ("Pharmacie Mendong", "Carrefour Mendong, Yaounde", [
        ("Paracetamol", 38), ("Ibuprofen", 20), ("Amoxicillin", 0), ("Metformin", 50), ("Amlodipine", 18),
    ]),
    ("Pharmacie Nlongkak", "Avenue Nlongkak, Yaounde", [
        ("Paracetamol", 72), ("Diclofenac", 33), ("Omeprazole", 27), ("Cetirizine", 40), ("Ibuprofen", 48),
    ]),
    ("Pharmacie Mvan", "Entrée Mvan, Yaounde", [
        ("Paracetamol", 100), ("Amoxicillin", 55), ("Metronidazole", 38), ("Vitamin C", 80), ("Aspirin", 35),
    ]),
    ("Pharmacie Emombo", "Rue Emombo, Yaounde", [
        ("Paracetamol", 28), ("Ibuprofen", 15), ("Artemether-Lumefantrine", 12), ("Chloroquine", 8), ("Ciprofloxacin", 20),
    ]),
    ("Pharmacie Tsinga", "Carrefour Tsinga, Yaounde", [
        ("Paracetamol", 60), ("Amoxicillin", 45), ("Metformin", 30), ("Amlodipine", 22), ("Omeprazole", 18),
    ]),
    ("Pharmacie Odza", "Avenue Odza, Yaounde", [
        ("Paracetamol", 85), ("Ibuprofen", 50), ("Cetirizine", 25), ("Diclofenac", 30), ("Vitamin C", 55),
    ]),
    ("Pharmacie Nkolbisson", "Campus Nkolbisson, Yaounde", [
        ("Paracetamol", 40), ("Amoxicillin", 35), ("Metronidazole", 28), ("Aspirin", 42), ("Ciprofloxacin", 15),
    ]),
    ("Pharmacie Ekounou", "Marché Ekounou, Yaounde", [
        ("Paracetamol", 95), ("Ibuprofen", 60), ("Omeprazole", 35), ("Metformin", 45), ("Amlodipine", 20),
    ]),
    ("Pharmacie Ntoussi", "Quartier Ntoussi, Yaounde", [
        ("Paracetamol", 50), ("Artemether-Lumefantrine", 18), ("Chloroquine", 10), ("Vitamin C", 65), ("Amoxicillin", 38),
    ]),
]

pharmacies: list[Pharmacy] = []
_next_med_id = 1
for pharmacy_id, (name, address, medications) in enumerate(DEMO_PHARMACIES, start=1):
    pharmacy = Pharmacy(pharmacy_id, name, address)
    for med_name, quantity in medications:
        pharmacy.add_medication(Medication(_next_med_id, med_name, quantity))
        _next_med_id += 1
    pharmacies.append(pharmacy)

pharmacist_user = Pharmacist(1, "Dr. Marie Nguema", "pharmacist@pharmafind.cm", "Pharmacie du Centre")
pharmacist_username = "pharmacist"
pharmacist_password = "pharma123"
pharmacist_tokens: set[str] = set()


def get_next_pharmacy_id() -> int:
    max_id = 0
    for pharmacy in pharmacies:
        if pharmacy.pharmacy_id > max_id:
            max_id = pharmacy.pharmacy_id
    return max_id + 1


def get_next_medication_id() -> int:
    max_id = 0
    for pharmacy in pharmacies:
        for medication in pharmacy.medications:
            if medication.med_id > max_id:
                max_id = medication.med_id
    return max_id + 1


@app.get("/")
def home():
    """Serve the frontend page."""
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/medications/search")
def search_medication(name: str = Query(..., description="Medication name to search")):
    """
    Search for a medication name across all pharmacies.
    This route appears automatically in Swagger UI at /docs.
    """
    results = []

    for pharmacy in pharmacies:
        found_medication = pharmacy.find_medication_by_name(name)
        if found_medication is not None:
            results.append(
                {
                    "pharmacy_id": pharmacy.pharmacy_id,
                    "pharmacy_name": pharmacy.name,
                    "address": pharmacy.address,
                    "medication_name": found_medication.name,
                    "quantity": found_medication.quantity,
                    "in_stock": found_medication.quantity > 0,
                }
            )

    return {"search": name, "results": results}


@app.get("/api/pharmacies")
def get_pharmacies():
    """Return all pharmacies (basic route for Swagger demo)."""
    items = []
    for pharmacy in pharmacies:
        items.append(
            {
                "pharmacy_id": pharmacy.pharmacy_id,
                "name": pharmacy.name,
                "address": pharmacy.address,
            }
        )
    return {"pharmacies": items}


@app.post("/api/pharmacist/login")
def pharmacist_login(payload: PharmacistLoginRequest):
    """
    Very simple login check for class project demo.
    """
    if payload.username != pharmacist_username or payload.password != pharmacist_password:
        raise HTTPException(status_code=401, detail="Invalid pharmacist credentials")

    token = str(uuid4())
    pharmacist_tokens.add(token)

    return {
        "message": "Login successful",
        "pharmacist_name": pharmacist_user.name,
        "role": pharmacist_user.get_role(),
        "token": token,
    }


@app.post("/api/pharmacies")
def add_pharmacy(
    payload: AddPharmacyRequest,
    pharmacist_token: str | None = Header(default=None, alias="X-Pharmacist-Token"),
):
    """
    Add a new pharmacy and one initial medication.
    """
    if pharmacist_token is None or pharmacist_token not in pharmacist_tokens:
        raise HTTPException(status_code=401, detail="Pharmacist login required")

    if payload.quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")

    new_pharmacy = Pharmacy(
        get_next_pharmacy_id(),
        payload.pharmacy_name.strip(),
        payload.address.strip(),
    )
    new_medication = Medication(
        get_next_medication_id(),
        payload.medication_name.strip(),
        payload.quantity,
    )
    new_pharmacy.add_medication(new_medication)
    pharmacies.append(new_pharmacy)

    return {
        "message": "Pharmacy added",
        "pharmacy_id": new_pharmacy.pharmacy_id,
        "pharmacy_name": new_pharmacy.name,
        "address": new_pharmacy.address,
        "first_medication": new_medication.name,
        "quantity": new_medication.quantity,
    }


@app.get("/api/pharmacies/{pharmacy_id}/medications")
def get_pharmacy_medications(pharmacy_id: int):
    """Return all medications for one pharmacy."""
    selected_pharmacy = None
    for pharmacy in pharmacies:
        if pharmacy.pharmacy_id == pharmacy_id:
            selected_pharmacy = pharmacy
            break

    if selected_pharmacy is None:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

    meds = []
    for medication in selected_pharmacy.medications:
        meds.append(
            {
                "med_id": medication.med_id,
                "name": medication.name,
                "quantity": medication.quantity,
                "in_stock": medication.quantity > 0,
            }
        )

    return {
        "pharmacy_id": selected_pharmacy.pharmacy_id,
        "pharmacy_name": selected_pharmacy.name,
        "medications": meds,
    }


@app.post("/api/pharmacies/{pharmacy_id}/stock")
def update_stock(
    pharmacy_id: int,
    payload: StockUpdateRequest,
    pharmacist_token: str | None = Header(default=None, alias="X-Pharmacist-Token"),
):
    """
    Update medication stock quantity for one pharmacy.
    This is used by pharmacist-side stock management.
    """
    if pharmacist_token is None or pharmacist_token not in pharmacist_tokens:
        raise HTTPException(status_code=401, detail="Pharmacist login required")

    if payload.new_quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")

    selected_pharmacy = None
    for pharmacy in pharmacies:
        if pharmacy.pharmacy_id == pharmacy_id:
            selected_pharmacy = pharmacy
            break

    if selected_pharmacy is None:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

    updated = selected_pharmacy.update_medication_stock(
        payload.medication_name, payload.new_quantity
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Medication not found in pharmacy")

    return {
        "message": "Stock updated",
        "pharmacy_id": selected_pharmacy.pharmacy_id,
        "medication_name": payload.medication_name,
        "new_quantity": payload.new_quantity,
    }
