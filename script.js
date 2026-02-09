/* ===========================
   QUICK IMAGE UPLOAD (HOME)
=========================== */
function goToStartWithImage() {
  const fileInput = document.getElementById("quickImage");

  if (!fileInput || fileInput.files.length === 0) {
    alert("Please upload an image first!");
    return;
  }

  localStorage.setItem("quickImageName", fileInput.files[0].name);
  window.location.href = "start.html";
}

/* ===========================
   MULTI STEP FORM + PROGRESS
=========================== */
const steps = document.querySelectorAll(".step");
const progressBar = document.getElementById("progressBar");
let currentStep = 0;

function showStep(index) {
  steps.forEach((step, i) => {
    step.classList.toggle("active", i === index);
  });

  if (progressBar) {
    const percent = ((index + 1) / steps.length) * 100;
    progressBar.style.width = percent + "%";
  }
}

document.querySelectorAll(".nextBtn").forEach(btn => {
  btn.addEventListener("click", () => {
    if (currentStep < steps.length - 1) {
      currentStep++;
      showStep(currentStep);
    }
  });
});

document.querySelectorAll(".prevBtn").forEach(btn => {
  btn.addEventListener("click", () => {
    if (currentStep > 0) {
      currentStep--;
      showStep(currentStep);
    }
  });
});

if (steps.length > 0) showStep(currentStep);

/* ===========================
   FORM SUBMIT (BACKEND)
=========================== */
document.getElementById("skinForm")?.addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = document.getElementById("skinForm");
  const formData = new FormData(form);

  const selectedConcerns = [];
  document.querySelectorAll("input[name='concerns']:checked").forEach(cb => {
    selectedConcerns.push(cb.value);
  });
  formData.append("concerns", selectedConcerns.join(", "));

  try {
    // Change this backend URL later
    const res = await fetch("BACKEND_API_URL/analyze", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    localStorage.setItem("result", JSON.stringify(data));
    window.location.href = "result.html";

  } catch (err) {
    // For now demo result (frontend only)
    const demoData = {
      skinType: formData.get("skinType"),
      concerns: selectedConcerns.join(", "),
      budget: formData.get("budget"),
      morningRoutine: ["Cleanser", "Moisturizer", "Sunscreen"],
      nightRoutine: ["Cleanser", "Treatment Serum", "Night Cream"],
      products: ["Vitamin C Serum", "Hydrating Moisturizer", "Sunscreen SPF 50"]
    };

    localStorage.setItem("result", JSON.stringify(demoData));
    window.location.href = "result.html";
  }
});

/* ===========================
   RESULT PAGE DISPLAY
=========================== */
window.addEventListener("load", () => {
  const resultBox = document.getElementById("resultBox");
  if (!resultBox) return;

  const data = JSON.parse(localStorage.getItem("result"));

  if (!data) {
    resultBox.innerHTML = "<p>No results found. Please submit the form first.</p>";
    return;
  }

  resultBox.innerHTML = `
    <h3>✨ Skin Type: ${data.skinType || "N/A"}</h3>
    <p><b>Concerns:</b> ${data.concerns || "N/A"}</p>
    <p><b>Budget:</b> ${data.budget || "N/A"}</p>

    <hr style="margin:15px 0; border:1px solid #eee;">

    <h4>🌞 Morning Routine</h4>
    <ul>
      ${(data.morningRoutine || []).map(item => `<li>${item}</li>`).join("")}
    </ul>

    <h4>🌙 Night Routine</h4>
    <ul>
      ${(data.nightRoutine || []).map(item => `<li>${item}</li>`).join("")}
    </ul>

    <h4>🧴 Recommended Products</h4>
    <ul>
      ${(data.products || []).map(p => `<li>${p}</li>`).join("")}
    </ul>
  `;
});

/* ===========================
   CHAT PAGE
=========================== */
function sendMsg() {
  const chatBox = document.getElementById("chatBox");
  const msgInput = document.getElementById("msg");

  if (!chatBox || !msgInput) return;

  const message = msgInput.value.trim();
  if (message === "") return;

  chatBox.innerHTML += `<p><b>You:</b> ${message}</p>`;
  chatBox.innerHTML += `<p><b>Aurelia:</b> Great question! For best results, follow a gentle routine and use sunscreen daily 💗</p>`;

  msgInput.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;
}

function quickAsk(text) {
  const msgInput = document.getElementById("msg");
  if (!msgInput) return;
  msgInput.value = text;
  sendMsg();
}

/* ===========================
   PRODUCTS PAGE FUNCTIONS
=========================== */
let routineItems = [];

function addToRoutine(productName) {
  if (!routineItems.includes(productName)) {
    routineItems.push(productName);
  }

  const list = document.getElementById("routineList");
  if (!list) return;

  list.innerHTML = routineItems.map(item => `<li>${item}</li>`).join("");
}

function clearRoutine() {
  routineItems = [];
  const list = document.getElementById("routineList");
  if (!list) return;
  list.innerHTML = "";
}

function filterProducts(category, btn) {
  const cards = document.querySelectorAll(".productCard");
  const buttons = document.querySelectorAll(".filterBtn");

  buttons.forEach(b => b.classList.remove("activeFilter"));
  if (btn) btn.classList.add("activeFilter");

  cards.forEach(card => {
    if (category === "all" || card.dataset.category === category) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });
}

function searchProducts() {
  const searchInput = document.getElementById("searchProduct");
  if (!searchInput) return;

  const searchValue = searchInput.value.toLowerCase();
  const cards = document.querySelectorAll(".productCard");

  cards.forEach(card => {
    const text = card.innerText.toLowerCase();
    card.style.display = text.includes(searchValue) ? "block" : "none";
  });
}
