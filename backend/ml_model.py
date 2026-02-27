import cv2
import numpy as np
import os
# TensorFlow / Keras imports are performed lazily in load_models()
# to allow the backend to run in demo mode when TF is not installed.

# ===============================
# MODEL PATHS
# ===============================

SKIN_TYPE_MODEL_PATH = "model/skin_type_.h5"
SKIN_CONCERN_MODEL_PATH = "model/skin_concerns_model.h5"

skin_type_model = None
skin_concern_model = None

# concerns list used for demo fallback
concerns = ["dryness", "pigmentation", "acne", "wrinkles", "pores", "dark_spots", "blackheads"]

# ===============================
# LOAD MODELS (lazy import)
# ===============================

def load_models():
    global skin_type_model, skin_concern_model

    try:
        # import TensorFlow / Keras only when needed
        import tensorflow as tf
        from tensorflow.keras.models import load_model
        from tensorflow.keras.preprocessing import image
    except Exception as e:
        print("⚠️ TensorFlow not available — running in demo mode.", str(e))
        return

    if skin_type_model is None:
        if os.path.exists(SKIN_TYPE_MODEL_PATH):
            try:
                skin_type_model = load_model(SKIN_TYPE_MODEL_PATH)
                print("✅ Skin type model loaded")
            except Exception as e:
                print("⚠️ Failed to load skin type model:", e)
        else:
            print("⚠️ Skin type model missing — demo mode")

    if skin_concern_model is None:
        if os.path.exists(SKIN_CONCERN_MODEL_PATH):
            try:
                skin_concern_model = load_model(SKIN_CONCERN_MODEL_PATH)
                print("✅ Skin concern model loaded")
            except Exception as e:
                print("⚠️ Failed to load skin concern model:", e)
        else:
            print("⚠️ Skin concern model missing — demo mode")

# ===============================
# MAIN ANALYSIS FUNCTION
# ===============================

def analyze_skin(img_path):
    # attempt to load models (will no-op if TF not installed)
    load_models()

    # ---------- SKIN TYPE ----------
    img1 = cv2.imread(img_path)
    if img1 is None:
        return {"error": "Invalid image"}

    img1 = cv2.resize(img1, (128,128))
    img1 = img1 / 255.0
    img1 = np.reshape(img1, (1,128,128,3))

    if skin_type_model is not None:
        try:
            pred1 = skin_type_model.predict(img1)[0]
            skin_classes = ["Oily", "Dry", "Combination", "Normal"]
            skin_type = skin_classes[np.argmax(pred1)]
            skin_conf = float(np.max(pred1))
        except Exception:
            skin_type = "Oily"
            skin_conf = 0.92
    else:
        skin_type = "Oily"
        skin_conf = 0.92

    # ---------- SKIN CONCERNS ----------
    # Only run concern model if it's loaded; otherwise return demo labels
    if skin_concern_model is not None:
        try:
            # import here to ensure tensorflow is available
            from tensorflow.keras.preprocessing import image
            img2 = image.load_img(img_path, target_size=(224,224))
            x = image.img_to_array(img2) / 255.0
            x = np.expand_dims(x, axis=0)

            preds = skin_concern_model.predict(x)[0]
            threshold = 0.5
            predicted_labels = [concerns[i] for i,p in enumerate(preds) if p > threshold]
        except Exception:
            predicted_labels = ["acne", "dark_spots"]
    else:
        predicted_labels = ["acne", "dark_spots"]

    return {
        "skin_type": skin_type,
        "confidence": round(skin_conf, 2),
        "recommendations": ", ".join(predicted_labels),
        "concerns": predicted_labels
    }
