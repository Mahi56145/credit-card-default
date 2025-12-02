import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import pandas as pd

def predict_single(sample: dict):
    """
    Run prediction on a single input sample.
    Example input:
    {
        "Income": 50000,
        "Age": 35,
        "Loan": 4000,
        "Loan to Income": 0.08
    }
    """
    # Load scaler + best model
    scaler = joblib.load("models/scaler_standard.joblib")
    model = joblib.load("models/best_model.joblib")

    df = pd.DataFrame([sample])
    scaled = scaler.transform(df)

    proba = model.predict_proba(scaled)[0][1]
    label = model.predict(scaled)[0]

    return {
        "probability_of_default": float(proba),
        "predicted_label": int(label)
    }


if __name__ == "__main__":
    # demo example
    test_sample = {
        "Income": 60000,
        "Age": 40,
        "Loan": 5000,
        "Loan to Income": 0.083
    }

    result = predict_single(test_sample)
    print("\nPrediction Result:")
    print(result)
