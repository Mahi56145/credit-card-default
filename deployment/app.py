# deployment/app.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import joblib
from pathlib import Path
import os

BASE = Path(__file__).resolve().parent.parent  # repo root
UI_DIST = BASE / "ui" / "dist"

app = FastAPI(title="Credit Card Default API")

# --- Static files mount ---
# Mount the entire ui/dist at /static so e.g. /static/index.html and /static/assets/* work.
if UI_DIST.exists():
    app.mount("/static", StaticFiles(directory=str(UI_DIST)), name="static")
else:
    # keep running but warn in logs
    print(f"WARNING: ui/dist not found at {UI_DIST!s}. Static UI will 404 until built.")

# --- Root route serves index.html from ui/dist ---
@app.get("/", response_class=JSONResponse)
def root():
    # keep JSON root for API; separate route for full UI below
    return {"status": "ok", "message": "Credit-card-default API. Open /docs for interactive API."}

@app.get("/ui", response_class=FileResponse)
def ui_index():
    index = UI_DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    raise HTTPException(status_code=404, detail="UI not found. Build the UI and ensure ui/dist/index.html exists.")

# convenience: serve same index at /static/index.html if needed (StaticFiles already does this if mounted correctly)
# (No extra route needed — this is just explicit fallback)
@app.get("/static/index.html", response_class=FileResponse)
def static_index():
    index = UI_DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    raise HTTPException(status_code=404, detail="UI not found.")

# --- Prediction request model (match your earlier model) ---
class PredictRequest(BaseModel):
    Income: float
    Age: float
    Loan: float
    Loan_to_Income: float  # use underscore name in request body

# --- lazy load model / scaler (use models/best_model.joblib etc.) ---
MODEL_PATH = BASE / "models" / "best_model.joblib"
SCALER_PATH = BASE / "models" / "scaler_standard.joblib"
_model = None
_scaler = None

def load_resources():
    global _model, _scaler
    if _model is None and MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    if _scaler is None and SCALER_PATH.exists():
        _scaler = joblib.load(SCALER_PATH)

@app.on_event("startup")
def startup_event():
    load_resources()
    print("App started. Routes:", [r.path for r in app.routes])
    print("UI_DIST:", str(UI_DIST))

@app.post("/predict")
def predict(req: PredictRequest):
    load_resources()
    if _model is None or _scaler is None:
        return {"error": "model or scaler not found. Check models/ folder."}

    import pandas as pd
    sample = pd.DataFrame([{
        "Income": req.Income,
        "Age": req.Age,
        "Loan": req.Loan,
        # scaler expects "Loan to Income" column if you trained with that name
        "Loan to Income": req.Loan_to_Income
    }])

    # if the scaler was trained with feature_names_in_ attribute, ensure columns match
    try:
        X = _scaler.transform(sample)
    except Exception:
        # attempt rename if needed
        if "Loan_to_Income" in sample.columns and "Loan to Income" in getattr(_scaler, "feature_names_in_", []):
            sample.rename(columns={"Loan_to_Income": "Loan to Income"}, inplace=True)
        X = _scaler.transform(sample)

    proba = float(_model.predict_proba(X)[:, 1][0])
    label = int(_model.predict(X)[0])
    return {"probability_of_default": proba, "predicted_label": label}
