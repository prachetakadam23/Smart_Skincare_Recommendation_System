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
   SKIN IMAGE ANALYSIS (START PAGE)
=========================== */
async function analyzeSkin(event) {
  if (event) event.preventDefault(); // Prevent form submission

  const fileInput = document.getElementById("imageInput");
  const resultBox = document.getElementById("result");

  if (!fileInput.files.length) {
    alert("Please upload an image first!");
    return;
  }

  resultBox.innerHTML = "<p>Analyzing skin image... 🔍</p>";

  try {
    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    resultBox.innerHTML = `
      <h4>✨ AI Skin Analysis Result</h4>
      <p><b>Skin Type:</b> ${data.skin_type || "N/A"}</p>
      <p><b>Confidence:</b> ${data.confidence ? (data.confidence * 100).toFixed(1) : "N/A"}%</p>
      ${data.recommendations ? `<p><b>Recommendations:</b> ${data.recommendations}</p>` : ""}
    `;

    // Optionally auto-fill skinType in form based on prediction
    const skinSelect = document.querySelector("select[name='skinType']");
    if (skinSelect && data.skin_type) {
      skinSelect.value = data.skin_type;
    }

  } catch (err) {
    console.error(err);
    resultBox.innerHTML =
      "<p style='color:red;'>Unable to connect to backend. Please try again later.</p>";
  }
}

/* ===========================
   MULTI STEP FORM + PROGRESS
=========================== */
const steps = document.querySelectorAll(".step");
const progressBar = document.getElementById("progressBar");
let currentStep = 0;

function showStep(index) {
  steps.forEach((step, i) => step.classList.toggle("active", i === index));

  if (progressBar) {
    const percent = ((index + 1) / steps.length) * 100;
    progressBar.style.width = percent + "%";
  }
}

document.querySelectorAll(".nextBtn").forEach(btn =>
  btn.addEventListener("click", () => {
    if (currentStep < steps.length - 1) {
      currentStep++;
      showStep(currentStep);
    }
  })
);

document.querySelectorAll(".prevBtn").forEach(btn =>
  btn.addEventListener("click", () => {
    if (currentStep > 0) {
      currentStep--;
      showStep(currentStep);
    }
  })
);

if (steps.length > 0) showStep(currentStep);

/* ===========================
   FORM SUBMIT (BACKEND WITH ML CONCERNS)
=========================== */
document.getElementById("skinForm")?.addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = document.getElementById("skinForm");
  const formData = new FormData(form);

  // Collect manually selected concerns
  const selectedConcerns = [];
  document.querySelectorAll("input[name='concerns']:checked").forEach(cb => {
    selectedConcerns.push(cb.value);
  });
  formData.append("concerns", selectedConcerns.join(","));

  try {
    const res = await fetch("http://127.0.0.1:5000/analyze_form", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    // Save combined concerns + predicted concerns to localStorage
    localStorage.setItem("result", JSON.stringify(data));
    window.location.href = "result.html";

  } catch (err) {
    console.error(err);

    // Demo fallback if backend fails
    const demoData = {
      skinType: formData.get("skinType"),
      concerns: selectedConcerns.join(","),
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
