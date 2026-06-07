const API_BASE = window.location.origin;

const pharmacistLoginBtn = document.getElementById("pharmacist-login-btn");
const logoutBtn = document.getElementById("logout-btn");
const closeLoginBtn = document.getElementById("close-login-btn");
const loginModal = document.getElementById("login-modal");
const loginStatus = document.getElementById("login-status");
const loginForm = document.getElementById("login-form");
const loginResult = document.getElementById("login-result");
const tabCustomer = document.getElementById("tab-customer");
const tabPharmacist = document.getElementById("tab-pharmacist");
const customerView = document.getElementById("customer-view");
const pharmacistView = document.getElementById("pharmacist-view");
const searchForm = document.getElementById("search-form");
const stockForm = document.getElementById("stock-form");
const addPharmacyForm = document.getElementById("add-pharmacy-form");
const viewMedsForm = document.getElementById("view-meds-form");
const refreshBtn = document.getElementById("refresh-btn");
const stockPharmacySelect = document.getElementById("stock-pharmacy-id");
const stockMedicationSelect = document.getElementById("stock-med-name");
const viewPharmacySelect = document.getElementById("view-pharmacy-id");
const searchResult = document.getElementById("search-result");
const stockResult = document.getElementById("stock-result");
const addPharmacyResult = document.getElementById("add-pharmacy-result");
const pharmacyList = document.getElementById("pharmacy-list");
const pharmacyMedsResult = document.getElementById("pharmacy-meds-result");

let pharmacistToken = null;

function makeStockLabel(quantity) {
  if (quantity > 0) return '<span class="status-in">In stock</span>';
  return '<span class="status-out">Out of stock</span>';
}

function openLoginModal() {
  loginResult.textContent = "";
  loginResult.className = "message-box";
  loginModal.classList.remove("hidden");
}

function showCustomerView() {
  tabCustomer.classList.add("active");
  tabPharmacist.classList.remove("active");
  customerView.classList.remove("hidden");
  pharmacistView.classList.add("hidden");
}

function showPharmacistView() {
  tabCustomer.classList.remove("active");
  tabPharmacist.classList.add("active");
  customerView.classList.add("hidden");
  pharmacistView.classList.remove("hidden");
}

function logout() {
  pharmacistToken = null;
  loginStatus.textContent = "Not logged in";
  pharmacistLoginBtn.classList.remove("hidden");
  logoutBtn.classList.add("hidden");
  tabPharmacist.classList.add("hidden");
  loginForm.reset();
  showCustomerView();
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

    stockPharmacySelect.innerHTML = "";
    viewPharmacySelect.innerHTML = "";
    for (const pharmacy of data.pharmacies) {
      const s = document.createElement("option");
      s.value = pharmacy.pharmacy_id;
      s.textContent = `${pharmacy.pharmacy_id} - ${pharmacy.name}`;
      stockPharmacySelect.appendChild(s);

      const v = document.createElement("option");
      v.value = pharmacy.pharmacy_id;
      v.textContent = `${pharmacy.pharmacy_id} - ${pharmacy.name}`;
      viewPharmacySelect.appendChild(v);
    }

    if (pharmacistToken) {
      await loadStockMedications(stockPharmacySelect.value);
    }
  } catch (error) {
    pharmacyList.textContent = "Error loading pharmacies.";
  }
}

async function loadStockMedications(pharmacyId) {
  stockMedicationSelect.innerHTML = "";
  if (!pharmacyId) return;
  try {
    const response = await fetch(`${API_BASE}/api/pharmacies/${pharmacyId}/medications`);
    const data = await response.json();
    if (!response.ok || !data.medications) return;

    for (const med of data.medications) {
      const option = document.createElement("option");
      option.value = med.name;
      option.textContent = `${med.name} (Qty: ${med.quantity})`;
      stockMedicationSelect.appendChild(option);
    }
  } catch (error) {
    stockResult.textContent = "Could not load medications for selected pharmacy.";
    stockResult.className = "message-box message-error";
  }
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const username = document.getElementById("login-username").value.trim();
  const password = document.getElementById("login-password").value;
  loginResult.textContent = "Checking login...";
  try {
    const response = await fetch(`${API_BASE}/api/pharmacist/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (!response.ok) {
      loginResult.textContent = data.detail || "Login failed";
      loginResult.className = "message-box message-error";
      return;
    }
    pharmacistToken = data.token;
    loginStatus.textContent = `Logged in as ${data.pharmacist_name}`;
    loginResult.textContent = "Login successful.";
    loginResult.className = "message-box message-success";
    loginModal.classList.add("hidden");
    pharmacistLoginBtn.classList.add("hidden");
    logoutBtn.classList.remove("hidden");
    tabPharmacist.classList.remove("hidden");
    await loadPharmacies();
    showPharmacistView();
  } catch (error) {
    loginResult.textContent = "Error checking login";
    loginResult.className = "message-box message-error";
  }
});

searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const medName = document.getElementById("med-name").value.trim();
  if (!medName) return;

  searchResult.textContent = "Searching...";
  try {
    const response = await fetch(`${API_BASE}/api/medications/search?name=${encodeURIComponent(medName)}`);
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
  const pharmacyId = stockPharmacySelect.value;
  const medicationName = stockMedicationSelect.value;
  const newQuantity = Number(document.getElementById("new-qty").value);
  stockResult.textContent = "Updating...";

  try {
    const response = await fetch(`${API_BASE}/api/pharmacies/${pharmacyId}/stock`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Pharmacist-Token": pharmacistToken,
      },
      body: JSON.stringify({ medication_name: medicationName, new_quantity: newQuantity }),
    });
    const data = await response.json();
    if (!response.ok) {
      stockResult.textContent = data.detail || "Failed to update stock.";
      stockResult.className = "message-box message-error";
      return;
    }
    stockResult.textContent = `Stock updated: ${data.medication_name} is now ${data.new_quantity}.`;
    stockResult.className = "message-box message-success";
    await loadPharmacies();
    await loadStockMedications(pharmacyId);
  } catch (error) {
    stockResult.textContent = "Error updating stock.";
    stockResult.className = "message-box message-error";
  }
});

addPharmacyForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const pharmacy_name = document.getElementById("new-pharmacy-name").value.trim();
  const address = document.getElementById("new-pharmacy-address").value.trim();
  const medication_name = document.getElementById("new-pharmacy-medication").value.trim();
  const quantity = Number(document.getElementById("new-pharmacy-quantity").value);
  addPharmacyResult.textContent = "Adding pharmacy...";

  try {
    const response = await fetch(`${API_BASE}/api/pharmacies`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Pharmacist-Token": pharmacistToken,
      },
      body: JSON.stringify({ pharmacy_name, address, medication_name, quantity }),
    });
    const data = await response.json();
    if (!response.ok) {
      addPharmacyResult.textContent = data.detail || "Failed to add pharmacy";
      addPharmacyResult.className = "message-box message-error";
      return;
    }
    addPharmacyResult.textContent = `Added ${data.pharmacy_name} successfully`;
    addPharmacyResult.className = "message-box message-success";
    addPharmacyForm.reset();
    document.getElementById("new-pharmacy-quantity").value = "10";
    await loadPharmacies();
  } catch (error) {
    addPharmacyResult.textContent = "Error adding pharmacy";
    addPharmacyResult.className = "message-box message-error";
  }
});

viewMedsForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const pharmacyId = viewPharmacySelect.value;
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

stockPharmacySelect.addEventListener("change", async () => {
  await loadStockMedications(stockPharmacySelect.value);
});
pharmacistLoginBtn.addEventListener("click", openLoginModal);
closeLoginBtn.addEventListener("click", () => loginModal.classList.add("hidden"));
logoutBtn.addEventListener("click", logout);
tabCustomer.addEventListener("click", showCustomerView);
tabPharmacist.addEventListener("click", showPharmacistView);
refreshBtn.addEventListener("click", loadPharmacies);
loadPharmacies();
