const API_BASE = window.location.origin;

const searchForm = document.getElementById("search-form");
const stockForm = document.getElementById("stock-form");
const viewMedsForm = document.getElementById("view-meds-form");
const refreshBtn = document.getElementById("refresh-btn");
const searchResult = document.getElementById("search-result");
const stockResult = document.getElementById("stock-result");
const pharmacyList = document.getElementById("pharmacy-list");
const pharmacyMedsResult = document.getElementById("pharmacy-meds-result");

function makeStockLabel(quantity) {
  if (quantity > 0) {
    return '<span class="status-in">In stock</span>';
  }
  return '<span class="status-out">Out of stock</span>';
}

async function loadPharmacies() {
  pharmacyList.textContent = "Loading pharmacies...";
  try {
    const response = await fetch(`${API_BASE}/api/pharmacies`);
    const data = await response.json();

    if (!data.pharmacies || data.pharmacies.length === 0) {
      pharmacyList.textContent = "No pharmacies found.";
      return;
    }

    let html = "<table><thead><tr><th>ID</th><th>Name</th><th>Address</th></tr></thead><tbody>";
    for (const pharmacy of data.pharmacies) {
      html += `<tr><td>${pharmacy.pharmacy_id}</td><td>${pharmacy.name}</td><td>${pharmacy.address}</td></tr>`;
    }
    html += "</tbody></table>";
    pharmacyList.innerHTML = html;
  } catch (error) {
    pharmacyList.textContent = "Error loading pharmacies.";
  }
}

searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const medName = document.getElementById("med-name").value.trim();
  if (!medName) return;

  searchResult.textContent = "Searching...";

  try {
    const response = await fetch(
      `${API_BASE}/api/medications/search?name=${encodeURIComponent(medName)}`
    );
    const data = await response.json();

    if (!data.results || data.results.length === 0) {
      searchResult.textContent = `No results found for "${medName}".`;
      return;
    }

    let html = "<table><thead><tr><th>Pharmacy</th><th>Address</th><th>Quantity</th><th>Status</th></tr></thead><tbody>";
    for (const item of data.results) {
      html += `<tr><td>${item.pharmacy_name}</td><td>${item.address}</td><td>${item.quantity}</td><td>${makeStockLabel(item.quantity)}</td></tr>`;
    }
    html += "</tbody></table>";
    searchResult.innerHTML = html;
  } catch (error) {
    searchResult.textContent = "Error loading search results.";
  }
});

stockForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const pharmacyId = document.getElementById("pharmacy-id").value;
  const medicationName = document.getElementById("stock-med-name").value.trim();
  const newQuantity = Number(document.getElementById("new-qty").value);

  stockResult.textContent = "Updating...";

  try {
    const response = await fetch(`${API_BASE}/api/pharmacies/${pharmacyId}/stock`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        medication_name: medicationName,
        new_quantity: newQuantity,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      stockResult.textContent = data.detail || "Failed to update stock.";
      return;
    }

    stockResult.textContent = `Stock updated: ${data.medication_name} is now ${data.new_quantity}.`;
    await loadPharmacies();
  } catch (error) {
    stockResult.textContent = "Error updating stock.";
  }
});

viewMedsForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const pharmacyId = document.getElementById("view-pharmacy-id").value;
  pharmacyMedsResult.textContent = "Loading medications...";

  try {
    const response = await fetch(`${API_BASE}/api/pharmacies/${pharmacyId}/medications`);
    const data = await response.json();

    if (!response.ok) {
      pharmacyMedsResult.textContent = data.detail || "Could not load medications.";
      return;
    }

    if (!data.medications || data.medications.length === 0) {
      pharmacyMedsResult.textContent = "No medications in this pharmacy.";
      return;
    }

    let html = `<p><strong>${data.pharmacy_name}</strong></p>`;
    html += "<table><thead><tr><th>Name</th><th>Quantity</th><th>Status</th></tr></thead><tbody>";
    for (const med of data.medications) {
      html += `<tr><td>${med.name}</td><td>${med.quantity}</td><td>${makeStockLabel(med.quantity)}</td></tr>`;
    }
    html += "</tbody></table>";
    pharmacyMedsResult.innerHTML = html;
  } catch (error) {
    pharmacyMedsResult.textContent = "Error loading medications.";
  }
});

refreshBtn.addEventListener("click", loadPharmacies);
loadPharmacies();
