from fastapi import FastAPI, Query

from backend.models import Medication, Pharmacy

app = FastAPI(
    title="Pharma-Find API",
    description="Simple API to search medication availability in pharmacies.",
    version="1.0.0",
)


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
    """Basic health route so the API has a simple entry point."""
    return {"message": "Welcome to Pharma-Find API"}


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
