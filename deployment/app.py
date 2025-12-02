# deployment/app.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import os
from pathlib import Path

# PROJECT ROOT (two levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent

# paths to ui build and models
UI_DIST_DIR = BASE_DIR / "ui" / "dist"
MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"
SCALER_PATH = BASE_DIR / "models" / "scaler_standard.joblib"

app = FastAPI(title="Credit Card Default API")

# -- mount static UI build at /static --
# This exposes:
#  - /static/index.html         -> ui/dist/index.html
#  - /static/assets/...         -> ui/dist/assets/...
if UI_DIST_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(UI_DIST_DIR)), name="static")
else:
    # warn in logs if UI files missing
    print(f"Warning: UI dist not found at {UI_DIST_DIR}. Build UI and place it there.")

# Root: serve the SPA index.html
@app.get("/")
def root():
    index_file = UI_DIST_DIR / "index.html"
    # if UI built, serve it; otherwise return a simple JSON
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"status": "ok", "message": "Credit-card-default API. Open /docs for interactive API."}

# Request model for predict
class PredictRequest(BaseModel):
    Income: float
    Age: float
    Loan: float
    # UI may send either Loan_to_Income OR "Loan to Income"; use underscore in model
    Loan_to_Income: float

# lazy-loaded model + scaler
_model = None
_scaler = None

def load_resources():
    global _model, _scaler
    if _model is None:
        if MODEL_PATH.exists():
            _model = joblib.load(str(MODEL_PATH))
            print("Loaded model:", MODEL_PATH)
        else:
            print("Model file missing:", MODEL_PATH)
    if _scaler is None:
        if SCALER_PATH.exists():
            _scaler = joblib.load(str(SCALER_PATH))
            print("Loaded scaler:", SCALER_PATH)
        else:
            print("Scaler missing:", SCALER_PATH)

@app.on_event("startup")
def startup_event():
    load_resources()
    print("App started. Routes:", [r.path for r in app.routes])

@app.post("/predict")
def predict(req: PredictRequest):
    load_resources()
    if _model is None or _scaler is None:
        raise HTTPException(500, detail="model or scaler not found on server. Check models/ folder.")

    import pandas as pd
    # build DataFrame using the same column names used when training
    sample = pd.DataFrame([{
        "Income": req.Income,
        "Age": req.Age,
        "Loan": req.Loan,
        # scaler previously expected column name "Loan to Income" (with space).
        # We'll create the space-name column if scaler expects it; otherwise keep underscore.
        "Loan to Income": req.Loan_to_Income
    }])

    # If scaler was fit with feature_names (sklearn >= 1.0) check and rename if needed
    try:
        if hasattr(_scaler, "feature_names_in_"):
            # if scaler expects underscore name, rename back to underscore
            if "Loan_to_Income" in _scaler.feature_names_in_ and "Loan to Income" in sample.columns:
                sample.rename(columns={"Loan to Income": "Loan_to_Income"}, inplace=True)
    except Exception:
        pass

    X = _scaler.transform(sample)
    proba = _model.predict_proba(X)[:, 1][0]
    label = int(_model.predict(X)[0])
    return {"probability_of_default": float(proba), "predicted_label": label}
