"""Flask web app that serves predictions from the trained CNN.

Mirrors the inference path from the training notebook:
  - Read image, resize to 128x128, convert BGR->RGB, normalize to [0,1]
  - Forward pass through the saved Keras model
  - Return class probabilities (top-5)
"""

import io
import json
import os
import time

import cv2
import numpy as np
from flask import Flask, jsonify, render_template, request

from disease_info import lookup

IMG_SIZE = 128
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "plant_disease_model.h5")
CLASSES_PATH = os.path.join(BASE_DIR, "model", "class_names.json")
HISTORY_PATH = os.path.join(BASE_DIR, "model", "history.json")
ALLOWED_EXTS = {"jpg", "jpeg", "png", "webp", "bmp"}
MAX_BYTES = 10 * 1024 * 1024  # 10 MB

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_BYTES

_model = None
_class_names = None


def get_model():
    global _model, _class_names
    if _model is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(CLASSES_PATH):
            raise FileNotFoundError(
                f"Model not found. Run `python train.py` first to produce {MODEL_PATH}."
            )
        from tensorflow.keras.models import load_model
        _model = load_model(MODEL_PATH)
        with open(CLASSES_PATH) as f:
            _class_names = json.load(f)
    return _model, _class_names


def preprocess_image(file_bytes):
    arr = np.frombuffer(file_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image. Use a JPG, PNG, or WebP file.")
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype("float32") / 255.0
    return np.expand_dims(img, axis=0)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTS


@app.route("/")
def index():
    model_ready = os.path.exists(MODEL_PATH) and os.path.exists(CLASSES_PATH)
    num_classes = 0
    if os.path.exists(CLASSES_PATH):
        try:
            with open(CLASSES_PATH) as f:
                num_classes = len(json.load(f))
        except Exception:
            num_classes = 0
    return render_template("index.html", model_ready=model_ready, num_classes=num_classes)


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "model_ready": os.path.exists(MODEL_PATH) and os.path.exists(CLASSES_PATH),
    })


@app.route("/api/info")
def info():
    if not os.path.exists(CLASSES_PATH):
        return jsonify({"model_ready": False, "classes": [], "history": None})
    with open(CLASSES_PATH) as f:
        classes = json.load(f)
    history = None
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH) as f:
            history = json.load(f)
    pretty = []
    for c in classes:
        meta = lookup(c)
        pretty.append({"raw": c, "plant": meta["plant"], "condition": meta["condition"], "status": meta["status"]})
    return jsonify({
        "model_ready": os.path.exists(MODEL_PATH),
        "num_classes": len(classes),
        "classes": pretty,
        "history": history,
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image field in request."}), 400
    f = request.files["image"]
    if not f or f.filename == "":
        return jsonify({"error": "Empty filename."}), 400
    if not allowed_file(f.filename):
        return jsonify({"error": f"Unsupported file type. Allowed: {sorted(ALLOWED_EXTS)}"}), 400

    raw = f.read()
    if not raw:
        return jsonify({"error": "Empty file."}), 400

    try:
        model, class_names = get_model()
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": f"Failed to load model: {e}"}), 500

    try:
        x = preprocess_image(raw)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    t0 = time.time()
    probs = model.predict(x, verbose=0)[0]
    elapsed_ms = int((time.time() - t0) * 1000)

    top_k = min(5, len(class_names))
    top_idx = np.argsort(probs)[::-1][:top_k]
    predictions = []
    for i in top_idx:
        cname = class_names[int(i)]
        meta = lookup(cname)
        predictions.append({
            "class": cname,
            "plant": meta["plant"],
            "condition": meta["condition"],
            "status": meta["status"],
            "description": meta["description"],
            "treatment": meta["treatment"],
            "confidence": float(probs[int(i)]),
        })
    return jsonify({
        "predictions": predictions,
        "top": predictions[0],
        "elapsed_ms": elapsed_ms,
        "image_size": IMG_SIZE,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
