"""
PlantCare AI — Flask application entry point.

Serves the web UI (home/upload, register, login, dashboard, result) and a
/predict endpoint that classifies an uploaded leaf image.

NOTE: model/plant_disease_model.h5 is currently a placeholder file (0 bytes).
Until a real trained model is added, /predict falls back to a demo response
so the UI can be exercised end-to-end. Swap in real inference by loading the
.h5 model with tensorflow.keras.models.load_model() and replacing
`mock_predict()` with a call to src/predict.py.
"""

import os
import random

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"

UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Demo label set + care tips, standing in for real model output until
# model/plant_disease_model.h5 is trained (see src/train.py).
DEMO_RESULTS = [
    {
        "crop": "Potato",
        "disease": "Early Blight",
        "confidence": 92,
        "tips": [
            "Remove and destroy infected leaves to slow spread.",
            "Apply a copper-based fungicide at the first sign of spots.",
            "Rotate crops next season to reduce soil-borne spores.",
        ],
    },
    {
        "crop": "Corn",
        "disease": "Rust",
        "confidence": 87,
        "tips": [
            "Improve air circulation by spacing plants further apart.",
            "Apply a fungicide labeled for rust if infection is widespread.",
            "Avoid overhead watering, which spreads spores between leaves.",
        ],
    },
    {
        "crop": "Grape",
        "disease": "Healthy",
        "confidence": 98,
        "tips": [
            "No action needed — keep up your current watering schedule.",
            "Continue routine scouting every 1–2 weeks.",
        ],
    },
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # TODO: persist the user (e.g. to a database) and hash the password.
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO: verify credentials against stored users.
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/predict", methods=["POST"])
def predict():
    uploaded = request.files.get("leaf_image")
    image_url = url_for("static", filename="img/sample-diseased.jpg")

    if uploaded and uploaded.filename:
        save_path = os.path.join(UPLOAD_FOLDER, uploaded.filename)
        uploaded.save(save_path)
        image_url = url_for("static", filename=f"uploads/{uploaded.filename}")

    result = mock_predict()
    return render_template(
        "result.html",
        image_url=image_url,
        crop=result["crop"],
        disease=result["disease"],
        confidence=result["confidence"],
        tips=result["tips"],
    )


def mock_predict():
    """Placeholder for src/predict.py + model/plant_disease_model.h5 inference."""
    return random.choice(DEMO_RESULTS)


if __name__ == "__main__":
    app.run(debug=True)
