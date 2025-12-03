from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import joblib
from pathlib import Path
import os
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("deployment.app")

BASE = Path(__file__).resolve().parent.parent
UI_DIST = BASE / "ui" / "dist"

app = FastAPI(title="Credit Card Default API")

if UI_DIST.exists():
    app.mount("/static", StaticFiles(directory=str(UI_DIST)), name="static")
else:
    log.warning("ui/dist not found at %s. Static UI will 404 until built.", UI_DIST)

@app.get("/", response_class=FileResponse)
def root_ui():
    index = UI_DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    return JSONResponse({"status": "ok", "message": "Credit-card-default API. Open /docs for interactive API."})

@app.get("/ui", response_class=FileResponse)
def ui_index():
    index = UI_DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    raise HTTPException(status_code=404, detail="UI not found. Build the UI and ensure ui/dist/index.html exists.")

@app.get("/static/index.html", response_class=FileResponse)
def static_index():
    index = UI_DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    raise HTTPException(status_code=404, detail="UI not found.")

class PredictRequest(BaseModel):
    Income: float
    Age: float
    Loan: float
    Loan_to_Income: float

MODEL_PATH = BASE / "models" / "best_model.joblib"
SCALER_PATH = BASE / "models" / "scaler_standard.joblib"
_model = None
_scaler = None

def get_model():
    global _model
    if _model is None:
        if MODEL_PATH.exists():
            log.info("Loading model from %s", MODEL_PATH)
            _model = joblib.load(MODEL_PATH)
        else:
            log.error("Model file missing: %s", MODEL_PATH)
    return _model

def get_scaler():
    global _scaler
    if _scaler is None:
        if SCALER_PATH.exists():
            log.info("Loading scaler from %s", SCALER_PATH)
            _scaler = joblib.load(SCALER_PATH)
        else:
            log.error("Scaler file missing: %s", SCALER_PATH)
    return _scaler

@app.on_event("startup")
def startup_event():
    log.info("App started. Routes: %s", [r.path for r in app.routes])
    log.info("UI_DIST: %s", str(UI_DIST))

@app.post("/predict")
def predict(req: PredictRequest):
    model = get_model()
    scaler = get_scaler()
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model or scaler not available on server. Check models/ folder.")

    import pandas as pd
    try:
        sample = pd.DataFrame([{
            "Income": req.Income,
            "Age": req.Age,
            "Loan": req.Loan,
            "Loan to Income": req.Loan_to_Income
        }])

        scaler_feature_names = getattr(scaler, "feature_names_in_", None)
        if scaler_feature_names is not None:
            missing = [c for c in scaler_feature_names if c not in sample.columns]
            if missing:
                rename_map = {}
                for expected in scaler_feature_names:
                    if expected.replace(" ", "_") in sample.columns:
                        rename_map[expected.replace(" ", "_")] = expected
                if rename_map:
                    sample = sample.rename(columns=rename_map)
            sample = sample.reindex(columns=scaler_feature_names)
        X = scaler.transform(sample)
        proba = float(model.predict_proba(X)[:, 1][0])
        label = int(model.predict(X)[0])
        return {"probability_of_default": proba, "predicted_label": label}
    except Exception as e:
        log.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
