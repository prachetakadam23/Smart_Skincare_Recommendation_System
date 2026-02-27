from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ml_model import analyze_skin
from nlp_model import get_chat_response
import joblib
from tensorflow.keras.models import load_model
import pandas as pd
from skincare_routine import get_complete_routine, enrich_routine_with_products, get_product_specific_routine

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

try:
    if os.path.exists(MODEL_PATH):
        concerns_model = load_model(MODEL_PATH)
        print("✅ Skin concern ML model loaded successfully")
    else:
        concerns_model = None
        print("⚠️  Model not found - running in demo mode with form-based concerns")
except Exception as e:
    concerns_model = None
    print(f"⚠️  Could not load model: {e} - running in demo mode")



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
    if not image.filename:
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
    skinType = request.json.get("skinType", "Normal")
    ageGroup = request.json.get("ageGroup", "")
    predicted_concerns = request.json.get("concerns", [])
    
    # Normalize concerns to lowercase for matching
    predicted_concerns = [c.lower().strip() for c in predicted_concerns]
    
    # Ensure concerns is not empty
    if not predicted_concerns:
        predicted_concerns = []
    
    # Get ALL products matching the selected concerns (not just top 3)
    all_products = get_all_products_for_concerns(predicted_concerns) if predicted_concerns else []
    
    # Create product-specific routines for each product
    product_routines = []
    if all_products:
        for product in all_products:
            try:
                routine = get_product_specific_routine(product, skinType)
                product_routines.append(routine)
            except Exception as e:
                print(f"Error creating routine for {product.get('product', 'Unknown')}: {e}")
                continue
    
    # Log for debugging
    print(f"\n📊 ANALYZE-FORM RESPONSE:")
    print(f"   Skin Type: {skinType}")
    print(f"   Concerns: {predicted_concerns}")
    print(f"   Products Found: {len(all_products)}")
    print(f"   Routines Generated: {len(product_routines)}")
    
    return jsonify({
        "skinType": skinType,
        "ageGroup": ageGroup,
        "concerns": predicted_concerns,
        "recommended_products": all_products,
        "product_routines": product_routines
    })
    

# ===========================
# Production frontend serving
# ===========================
# When the React app is built (`npm run build`), the output lands in
# `frontend/dist`.  The Flask server can serve those files so that the
# application is self‑contained (useful for simple deployments).
#
# After building, start the backend normally (`python app.py`) and the
# same server will handle API requests and return the SPA.
from flask import send_from_directory

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Return the React build assets or index.html for SPA routing."""
    dist_dir = os.path.join(BASE_DIR, 'frontend', 'dist')
    if path and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)
    return send_from_directory(dist_dir, 'index.html')



# ===========================
# Chat endpoint
# ===========================
@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "")
    
    if not user_msg:
        return jsonify({"error": "No message provided"}), 400
    
    # Use NLP model to generate response
    reply = get_chat_response(user_msg)
    
    return jsonify({"reply": reply})

# ===========================
# Load skincare product dataset (CSV)
# ===========================

DATASET_PATH = os.path.join(BASE_DIR, "datasets", "skincare_products.csv")

print("🔎 Looking for dataset at:", DATASET_PATH)

product_df = None
if os.path.exists(DATASET_PATH):
    try:
        # Try multiple encodings to handle different character sets
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        product_df = None
        
        for encoding in encodings:
            try:
                product_df = pd.read_csv(DATASET_PATH, encoding=encoding)
                break
            except Exception:
                continue
        
        if product_df is None:
            raise Exception("Could not decode CSV with any supported encoding")
        
        # Clean column names
        product_df.columns = product_df.columns.str.lower().str.strip()
        # Rename columns to match expected names
        column_mapping = {
            'product_name': 'product',
            'product_description': 'description',
            'price_range (inr)': 'price',
            'ingredients': 'ingredients'
        }
        product_df.rename(columns=column_mapping, inplace=True)
        print(f"✅ Skincare product dataset loaded successfully ({len(product_df)} products)")
        print(f"Columns: {list(product_df.columns)}")
    except Exception as e:
        print(f"❌ Error loading CSV dataset: {e}")
        product_df = None
else:
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

    # Select top products (first one per concern, max top_n)
    results = []
    seen_concerns = set()
    
    for _, row in matched.iterrows():
        concern = row["concern"]
        if concern not in seen_concerns and len(results) < top_n:
            seen_concerns.add(concern)
            results.append({
                "product": row.get("product", ""),
                "description": row.get("description", ""),
                "ingredients": row.get("ingredients", ""),
                "price": row.get("price", ""),
                "concern": concern
            })
    
    return results


def get_all_products_for_concerns(concerns):
    """
    Get ALL products for the given concerns (not limited to top_n).
    Returns all matching products organized by concern.
    """
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

    # Return all matching products
    results = []
    for _, row in matched.iterrows():
        results.append({
            "product": row.get("product", ""),
            "description": row.get("description", ""),
            "ingredients": row.get("ingredients", ""),
            "price": row.get("price", ""),
            "concern": row.get("concern", "")
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
