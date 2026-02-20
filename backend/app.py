from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ml_model import analyze_skin
import joblib
from tensorflow.keras.models import load_model
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ===========================
# Load trained models
# ===========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "skin_concerns_model.h5")

print("🔎 Looking for model at:", MODEL_PATH)


if os.path.exists(MODEL_PATH):
    concerns_model = load_model(MODEL_PATH)
    print("✅ Skin concern ML model loaded successfully")
else:
    concerns_model = None
    print("❌ Model NOT found at:", MODEL_PATH)



# ===========================
# Home route
# ===========================
@app.route('/')
def home():
    return "Aurelia Backend Running 🚀"

# ===========================
# Analyze uploaded image
# ===========================
@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(file_path)

    result = analyze_skin(file_path)
    return jsonify(result)

# ===========================
# Analyze form (skin + concerns)
# ===========================
@app.route("/analyze-form", methods=["POST"])
def analyze_form():
    skinType = request.json.get("skinType")
    ageGroup = request.json.get("ageGroup")
    predicted_concerns = request.json.get("concerns", [])
    products = recommend_products(predicted_concerns)
    
    return jsonify({
    "skinType": skinType,
    "ageGroup": ageGroup,
    "concerns": predicted_concerns,
    "recommended_products": products
    })
    


# ===========================
# Chat endpoint
# ===========================
@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message")
    reply = f"For {user_msg}, I recommend cleanser, serum & sunscreen 💗"
    return jsonify({"reply": reply})

# ===========================
# Load skincare product dataset
# ===========================

DATASET_PATH = os.path.join(BASE_DIR, "datasets", "skincare_products.csv")

print("🔎 Looking for dataset at:", DATASET_PATH)

if os.path.exists(DATASET_PATH):
    try:
        product_df = pd.read_csv(DATASET_PATH, encoding="utf-8")
        product_df["rating"] = product_df["rating"].fillna(product_df["rating"].mean())
    except UnicodeDecodeError:
        product_df = pd.read_csv(DATASET_PATH, encoding="latin1")

    print("✅ Skincare product dataset loaded successfully")
else:
    product_df = None
    print("❌ Skincare product dataset NOT found")


def recommend_products(concerns, top_n=3):
    if product_df is None:
        return []

    # Normalize text
    concerns = [c.lower().strip() for c in concerns]

    df = product_df.copy()
    df["concern"] = df["concern"].str.lower()


    # Filter products matching concerns
    matched = df[df["concern"].isin(concerns)]

    if matched.empty:
        return []

    # Sort by rating (desc) then price (asc)
    matched = matched.sort_values(
        by=["rating", "price_range (INR)"],
        ascending=[False, True]
    )

    results = []
    for _, row in matched.head(top_n).iterrows():
        results.append({
            "product_name": row["product_name"],
            "description": row["product_description"],
            "ingredients": row["ingredients"],
            "price": row["price_range (INR)"],
            "rating": row["rating"]
        })

    return results
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    concerns = data.get("concerns", [])

    products = recommend_products(concerns)

    return jsonify({
        "concerns": concerns,
        "recommendations": products
    })



# ===========================
# Run Flask
# ===========================
if __name__ == '__main__':
    app.run(debug=True)
