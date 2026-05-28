from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.models import Medication, Pharmacy

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


# In-memory sample data for now (simple for class project step-by-step build).
pharmacy_a = Pharmacy(1, "CityCare Pharmacy", "12 Main Street")
pharmacy_a.add_medication(Medication(1, "Paracetamol", 20))
pharmacy_a.add_medication(Medication(2, "Ibuprofen", 0))

pharmacy_b = Pharmacy(2, "HealthPlus Pharmacy", "48 Queen Avenue")
pharmacy_b.add_medication(Medication(3, "Paracetamol", 6))
pharmacy_b.add_medication(Medication(4, "Amoxicillin", 12))

pharmacies = [pharmacy_a, pharmacy_b]


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


@app.post("/api/pharmacies/{pharmacy_id}/stock")
def update_stock(pharmacy_id: int, payload: StockUpdateRequest):
    """
    Update medication stock quantity for one pharmacy.
    This is used by pharmacist-side stock management.
    """
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
