const API_BASE = "https://sen-2241-pharma-find-nquqbo3f6-mohammad-awals-projects-e2736a33.vercel.app";

const searchForm = document.getElementById("search-form");
const stockForm = document.getElementById("stock-form");
const searchResult = document.getElementById("search-result");
const stockResult = document.getElementById("stock-result");

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

    const lines = data.results.map(
      (item) =>
        `${item.pharmacy_name} (${item.address}) - Qty: ${item.quantity} - ${
          item.in_stock ? "In stock" : "Out of stock"
        }`
    );
    searchResult.textContent = lines.join("\n");
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
  } catch (error) {
    stockResult.textContent = "Error updating stock.";
  }
});
