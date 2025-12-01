import joblib
import pandas as pd

def load_model_and_scaler(model_path="models/best_model.joblib", scaler_path="models/scaler_standard.joblib"):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict_sample(sample_dict, model, scaler):
    df = pd.DataFrame([sample_dict])
    sample_ordered = df  # assume columns match training order
    scaled = scaler.transform(sample_ordered)
    pred_proba = model.predict_proba(scaled)[:, 1][0]
    pred_label = int(model.predict(scaled)[0])
    return {"probability": float(pred_proba), "label": pred_label}
