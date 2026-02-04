// 🔌 CONFIGURAZIONE API BACKEND
const API_BASE_URL = "http://localhost:8000";

// 🔐 Gestione autenticazione
let authToken = localStorage.getItem("authToken");
let currentUser = null;
let allRecipes = []; // Cache delle ricette
let currentGenre = null; // Filtro genere attivo

// 🌐 Utility: chiamata API con autenticazione
async function apiCall(endpoint, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (authToken) {
    headers["Authorization"] = `Bearer ${authToken}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Token scaduto, logout
    logout();
    throw new Error("Sessione scaduta. Effettua nuovamente il login.");
  }

  return response;
}

// 📚 Carica ricette dal backend
async function loadRecipes(genreId = null) {
  try {
    let url = "/api/recipes";
    if (genreId) {
      url += `?genre_id=${genreId}`;
    }
    
    const response = await apiCall(url);
    if (!response.ok) throw new Error("Errore caricamento ricette");

    const recipes = await response.json();
    allRecipes = recipes;
    currentGenre = genreId;
    displayRecipes(recipes);
  } catch (error) {
    console.error("Errore:", error);
    showError("Impossibile caricare le ricette. Assicurati che il backend sia avviato.");
  }
}

// 🎨 Mostra ricette nella grid
function displayRecipes(recipes) {
  const grid = document.querySelector(".grid");
  
  if (!recipes || recipes.length === 0) {
    grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; padding: 2rem;">Nessuna ricetta trovata</p>';
    return;
  }

  grid.innerHTML = recipes
    .map(
      (recipe) => `
    <article class="card" onclick="showRecipeDetail(${recipe.ID})" style="cursor: pointer;">
      <div class="card-media" style="background-image: url('${recipe.main_image || ""}')"></div>
      <div class="card-body">
        <h3>${recipe.titolo}</h3>
        <p>${recipe.descrizione || "Ricetta tradizionale italiana"}</p>
        <div class="card-actions">
          <span class="tag">${recipe.tempo_preparazione || "N/A"} min</span>
          <span class="tag">Difficoltà: ${recipe.difficolta || "Media"}</span>
          <button class="btn btn-secondary" onclick="event.stopPropagation(); addToCart(${recipe.ID})">Aggiungi</button>
        </div>
      </div>
    </article>
  `
    )
    .join("");

  // Aggiungi animazioni alle card
  addCardAnimations();
}

// ✨ Animazioni card (codice originale)
function addCardAnimations() {
  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.style.transform = "translateY(-4px)";
      card.style.transition = "transform 0.2s ease";
    });

    card.addEventListener("mouseleave", () => {
      card.style.transform = "translateY(0)";
    });
  });
}

// 🔑 Login utente
async function login(email, password) {
  try {
    const response = await apiCall("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) throw new Error("Credenziali non valide");

    const data = await response.json();
    authToken = data.access_token;
    localStorage.setItem("authToken", authToken);
    currentUser = data.user;

    closeAuthModal();
    showToast("Login effettuato con successo!", "success");
    updateUI();
  } catch (error) {
    console.error("Errore login:", error);
    showToast("Email o password non corretti", "error");
  }
}

// 📝 Registrazione utente
async function register(nome, email, password, telefono = "") {
  try {
    const response = await apiCall("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ 
        nome, 
        email, 
        password,
        telefono: telefono || undefined 
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Errore durante la registrazione");
    }

    const data = await response.json();
    authToken = data.access_token;
    localStorage.setItem("authToken", authToken);
    currentUser = data.user;

    closeAuthModal();
    showToast("Account creato con successo!", "success");
    updateUI();
  } catch (error) {
    console.error("Errore registrazione:", error);
    showToast(error.message || "Impossibile creare l'account", "error");
  }
}

// 🚪 Logout
function logout() {
  authToken = null;
  currentUser = null;
  localStorage.removeItem("authToken");
  updateUI();
  showToast("Logout effettuato", "success");
}

// 🛒 Aggiungi al carrello
let selectedRecipeId = null;

async function addToCart(recipeId) {
  if (!authToken) {
    showToast("Devi effettuare il login per aggiungere ricette al carrello", "error");
    showAuthModal();
    return;
  }

  selectedRecipeId = recipeId;
  showPersonsModal();
}

// Mostra modal numero persone
function showPersonsModal() {
  document.getElementById("persons-modal").classList.add("active");
  document.getElementById("persons-count").value = 2;
  document.getElementById("persons-count").focus();
}

function closePersonsModal() {
  document.getElementById("persons-modal").classList.remove("active");
  selectedRecipeId = null;
}

// Gestione form numero persone
document.getElementById("persons-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const persone = parseInt(document.getElementById("persons-count").value);
  
  if (persone < 1) {
    showToast("Numero di persone non valido", "error");
    return;
  }

  try {
    const response = await apiCall("/api/cart/items", {
      method: "POST",
      body: JSON.stringify({ 
        recipe_id: selectedRecipeId, 
        persone: persone
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Errore aggiunta al carrello");
    }

    const result = await response.json();
    showToast(`Ricetta aggiunta al carrello! Prezzo: €${result.prezzo_calcolato.toFixed(2)}`, "success");
    closePersonsModal();
    updateCartCount();
  } catch (error) {
    console.error("Errore:", error);
    showToast(error.message || "Impossibile aggiungere al carrello", "error");
  }
});

// 🔢 Aggiorna contatore carrello
async function updateCartCount() {
  const cartBtn = document.querySelector(".btn-primary");
  if (!authToken) {
    cartBtn.textContent = "Carrello (0)";
    cartBtn.onclick = showCartModal;
    return;
  }

  try {
    const response = await apiCall("/api/cart");
    if (!response.ok) return;

    const cart = await response.json();
    const count = cart.count || 0;
    cartBtn.textContent = `Carrello (${count})`;
    cartBtn.onclick = showCartModal;
  } catch (error) {
    console.error("Errore aggiornamento carrello:", error);
  }
}

// 🛍️ Mostra modal carrello
async function showCartModal() {
  if (!authToken) {
    showToast("Effettua il login per visualizzare il carrello", "error");
    showAuthModal();
    return;
  }

  try {
    const response = await apiCall("/api/cart");
    if (!response.ok) throw new Error("Impossibile caricare il carrello");

    const cart = await response.json();
    const cartItemsList = document.getElementById("cart-items-list");
    const cartTotalAmount = document.getElementById("cart-total-amount");

    if (cart.count === 0) {
      cartItemsList.innerHTML = `
        <div class="empty-cart">
          <div class="empty-cart-icon">🛒</div>
          <p>Il tuo carrello è vuoto</p>
          <p style="font-size: 0.9rem; margin-top: 8px;">Aggiungi delle ricette per iniziare!</p>
        </div>
      `;
      cartTotalAmount.textContent = "€0.00";
    } else {
      cartItemsList.innerHTML = cart.items.map(item => `
        <div class="cart-item">
          <div class="cart-item-info">
            <h4>${item.recipe.titolo}</h4>
            <p>Per ${item.persone} ${item.persone > 1 ? 'persone' : 'persona'}</p>
            ${item.wine ? `<p><small>🍷 ${item.wine.nome}</small></p>` : ''}
          </div>
          <div class="cart-item-actions">
            <span class="cart-item-price">€${parseFloat(item.prezzo_item).toFixed(2)}</span>
            <button class="btn btn-small" onclick="removeCartItem(${item.ID})">✕</button>
          </div>
        </div>
      `).join('');
      cartTotalAmount.textContent = `€${parseFloat(cart.totale).toFixed(2)}`;
    }

    document.getElementById("cart-modal").classList.add("active");
  } catch (error) {
    console.error("Errore:", error);
    showToast("Impossibile caricare il carrello", "error");
  }
}

function closeCartModal() {
  document.getElementById("cart-modal").classList.remove("active");
}

// 🗑️ Rimuovi item dal carrello
async function removeCartItem(itemId) {
  try {
    const response = await apiCall(`/api/cart/items/${itemId}`, {
      method: "DELETE",
    });

    if (!response.ok) throw new Error("Impossibile rimuovere l'item");

    showToast("Ricetta rimossa dal carrello", "success");
    updateCartCount();
    showCartModal(); // Ricarica il carrello
  } catch (error) {
    console.error("Errore:", error);
    showToast("Impossibile rimuovere l'item", "error");
  }
}

// 💳 Mostra modal checkout
async function showCheckoutModal() {
  try {
    const response = await apiCall("/api/cart");
    if (!response.ok) throw new Error("Impossibile caricare il carrello");

    const cart = await response.json();
    
    if (cart.count === 0) {
      showToast("Il carrello è vuoto", "error");
      return;
    }

    document.getElementById("checkout-total").textContent = `€${parseFloat(cart.totale).toFixed(2)}`;
    document.getElementById("checkout-items-count").textContent = `${cart.count} ${cart.count > 1 ? 'ricette' : 'ricetta'} nel carrello`;
    
    closeCartModal();
    document.getElementById("checkout-modal").classList.add("active");
    document.getElementById("checkout-address").focus();
  } catch (error) {
    console.error("Errore:", error);
    showToast("Impossibile procedere al checkout", "error");
  }
}

function closeCheckoutModal() {
  document.getElementById("checkout-modal").classList.remove("active");
  document.getElementById("checkout-form").reset();
}

// Gestione form checkout
document.getElementById("checkout-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const indirizzo = document.getElementById("checkout-address").value;
  
  if (indirizzo.length < 10) {
    showToast("Indirizzo troppo corto (minimo 10 caratteri)", "error");
    return;
  }

  try {
    const response = await apiCall("/api/cart/checkout", {
      method: "POST",
      body: JSON.stringify({ indirizzo_consegna: indirizzo }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Errore durante il checkout");
    }

    const order = await response.json();
    closeCheckoutModal();
    showToast(`Ordine #${order.ID} creato con successo! Totale: €${parseFloat(order.totale).toFixed(2)}`, "success");
    updateCartCount();
  } catch (error) {
    console.error("Errore:", error);
    showToast(error.message || "Impossibile completare l'ordine", "error");
  }
});

// 🎭 Aggiorna UI in base allo stato di autenticazione
function updateUI() {
  const loginBtn = document.querySelector(".btn");
  if (currentUser) {
    loginBtn.textContent = `Ciao, ${currentUser.nome}`;
    loginBtn.onclick = logout;
  } else {
    loginBtn.textContent = "Login";
    loginBtn.onclick = showAuthModal;
  }
  updateCartCount();
}

// 🎭 Modal Login/Register
function showAuthModal() {
  document.getElementById("auth-modal").classList.add("active");
}

function closeAuthModal() {
  document.getElementById("auth-modal").classList.remove("active");
}

function switchAuthTab(tab) {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const tabs = document.querySelectorAll(".auth-tab");

  tabs.forEach(t => t.classList.remove("active"));
  
  if (tab === "login") {
    loginForm.style.display = "block";
    registerForm.style.display = "none";
    tabs[0].classList.add("active");
  } else {
    loginForm.style.display = "none";
    registerForm.style.display = "block";
    tabs[1].classList.add("active");
  }
}

// ✅ Notifica toast moderna
function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = "slideOutRight 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Vecchie funzioni di notifica (retrocompatibilità)
function showSuccess(message) {
  showToast(message, "success");
}

function showError(message) {
  showToast(message, "error");
}

//  Setup ricerca (nuovo, sostituisce il vecchio)
function setupSearch() {
  const searchInput = document.querySelector('input[type="text"]');
  if (!searchInput) return;

  searchInput.placeholder = "Cerca una ricetta...";
  let searchTimeout;

  searchInput.addEventListener("input", (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      const searchTerm = e.target.value.toLowerCase().trim();
      
      if (!searchTerm) {
        displayRecipes(allRecipes);
        return;
      }

      const filtered = allRecipes.filter(recipe => 
        recipe.titolo.toLowerCase().includes(searchTerm) ||
        (recipe.descrizione && recipe.descrizione.toLowerCase().includes(searchTerm))
      );

      displayRecipes(filtered);
    }, 300); // Debounce 300ms
  });
}

// 🍽️ Mostra dettagli ricetta
async function showRecipeDetail(recipeId) {
  try {
    const response = await apiCall(`/api/recipes/${recipeId}`);
    if (!response.ok) throw new Error("Impossibile caricare i dettagli");

    const recipe = await response.json();
    const content = document.getElementById("recipe-detail-content");

    content.innerHTML = `
      <div class="recipe-detail-header">
        ${recipe.main_image ? `<img src="${recipe.main_image}" alt="${recipe.titolo}" class="recipe-detail-image">` : ''}
      </div>
      
      <div class="recipe-detail-body">
        <h2 class="recipe-detail-title">${recipe.titolo}</h2>
        
        <div class="recipe-detail-meta">
          <div class="recipe-detail-meta-item">
            <span>⏱️</span>
            <span>${recipe.tempo_preparazione || 'N/A'} minuti</span>
          </div>
          <div class="recipe-detail-meta-item">
            <span>👨‍🍳</span>
            <span>Difficoltà: ${recipe.difficolta || 'Media'}</span>
          </div>
          <div class="recipe-detail-meta-item">
            <span>👥</span>
            <span>Prezzo base per persona</span>
          </div>
        </div>

        ${recipe.descrizione ? `
          <div class="recipe-detail-section">
            <h3>📝 Descrizione</h3>
            <div class="recipe-description">${recipe.descrizione}</div>
          </div>
        ` : ''}

        ${recipe.ingredienti && recipe.ingredienti.length > 0 ? `
          <div class="recipe-detail-section">
            <h3>🥘 Ingredienti (per persona)</h3>
            <ul class="ingredients-list">
              ${recipe.ingredienti.map(ing => `
                <li>
                  <span class="ingredient-name">${ing.nome}</span>
                  <span class="ingredient-quantity">${parseFloat(ing.quantita_per_persona).toFixed(2)} ${ing.unita_misura}</span>
                </li>
              `).join('')}
            </ul>
          </div>
        ` : ''}

        ${recipe.vini && recipe.vini.length > 0 ? `
          <div class="recipe-detail-section">
            <h3>🍷 Vini abbinabili</h3>
            <ul class="wines-list">
              ${recipe.vini.map(vino => `
                <li>
                  <div>
                    <div class="wine-name">${vino.nome}</div>
                    <small style="color: var(--muted);">${vino.tipo || ''}</small>
                  </div>
                  <span class="wine-price">€${parseFloat(vino.prezzo).toFixed(2)}</span>
                </li>
              `).join('')}
            </ul>
          </div>
        ` : ''}

        <div class="recipe-detail-footer">
          <div class="recipe-detail-price">
            €${recipe.prezzo_base_porzione ? parseFloat(recipe.prezzo_base_porzione).toFixed(2) : '0.00'}
            <small>/ persona</small>
          </div>
          <button class="btn btn-primary" onclick="closeRecipeModal(); addToCart(${recipe.ID})">
            Aggiungi al carrello
          </button>
        </div>
      </div>
    `;

    document.getElementById("recipe-modal").classList.add("active");
  } catch (error) {
    console.error("Errore:", error);
    showToast("Impossibile caricare i dettagli della ricetta", "error");
  }
}

function closeRecipeModal() {
  document.getElementById("recipe-modal").classList.remove("active");
}

// 🔍 Carica generi per filtri
async function loadGenres() {
  try {
    const response = await apiCall("/api/recipes/genres");
    if (!response.ok) return;

    const genres = await response.json();
    const filtersContainer = document.querySelector(".filters");
    
    if (!filtersContainer) return;

    // Pulsante "Tutti"
    const allButton = document.createElement("button");
    allButton.className = "btn" + (!currentGenre ? " btn-primary" : "");
    allButton.textContent = "Tutti";
    allButton.onclick = () => filterByGenre(null);
    filtersContainer.appendChild(allButton);

    // Pulsanti per ogni genere
    genres.forEach(genre => {
      const button = document.createElement("button");
      button.className = "btn" + (currentGenre === genre.ID ? " btn-primary" : "");
      button.textContent = genre.nome;
      button.onclick = () => filterByGenre(genre.ID);
      filtersContainer.appendChild(button);
    });
  } catch (error) {
    console.error("Errore caricamento generi:", error);
  }
}

function filterByGenre(genreId) {
  currentGenre = genreId;
  loadRecipes(genreId);
}

// 📜 Scroll al catalogo (pulsante "Esplora")
function scrollToCatalog() {
  const catalogSection = document.querySelector(".container");
  if (catalogSection) {
    catalogSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

// 🚀 Inizializzazione app
async function init() {
  console.log("🚀 Connessione al backend:", API_BASE_URL);

  // Verifica connessione backend
  try {
    const response = await fetch(`${API_BASE_URL}/docs`);
    if (response.ok) {
      console.log("✅ Backend connesso!");
    } else {
      console.warn("⚠️ Backend non risponde correttamente");
    }
  } catch (error) {
    console.error("❌ Backend non raggiungibile:", error);
    showError(
      "Backend non disponibile. Assicurati che sia avviato su http://localhost:8000"
    );
  }

  // Carica dati iniziali
  await loadRecipes();
  await loadGenres();
  setupSearch();
  updateUI();
  
  // Setup form listeners
  document.getElementById("login-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
    login(email, password);
  });
  
  document.getElementById("register-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const nome = document.getElementById("register-nome").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const telefono = document.getElementById("register-telefono").value;
    register(nome, email, password, telefono);
  });
  
  // Chiudi modal con click fuori
  document.getElementById("auth-modal").addEventListener("click", (e) => {
    if (e.target.id === "auth-modal") {
      closeAuthModal();
    }
  });
  
  document.getElementById("persons-modal").addEventListener("click", (e) => {
    if (e.target.id === "persons-modal") {
      closePersonsModal();
    }
  });
  
  document.getElementById("cart-modal").addEventListener("click", (e) => {
    if (e.target.id === "cart-modal") {
      closeCartModal();
    }
  });
  
  document.getElementById("checkout-modal").addEventListener("click", (e) => {
    if (e.target.id === "checkout-modal") {
      closeCheckoutModal();
    }
  });
  
  document.getElementById("recipe-modal").addEventListener("click", (e) => {
    if (e.target.id === "recipe-modal") {
      closeRecipeModal();
    }
  });
}

// 🎬 Avvia app quando DOM è pronto
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}

// Rendi funzioni globali per onclick
window.addToCart = addToCart;
window.showAuthModal = showAuthModal;
window.closeAuthModal = closeAuthModal;
window.switchAuthTab = switchAuthTab;
window.showRecipeDetail = showRecipeDetail;
window.closeRecipeModal = closeRecipeModal;
window.showCartModal = showCartModal;
window.closeCartModal = closeCartModal;
window.removeCartItem = removeCartItem;
window.showCheckoutModal = showCheckoutModal;
window.closeCheckoutModal = closeCheckoutModal;
window.showPersonsModal = showPersonsModal;
window.closePersonsModal = closePersonsModal;
window.scrollToCatalog = scrollToCatalog;
window.filterByGenre = filterByGenre;
