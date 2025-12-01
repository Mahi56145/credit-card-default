from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import load_model_and_scaler, predict_sample

app = FastAPI(title="Credit Default API")

class InputData(BaseModel):
    Income: float
    Age: float
    Loan: float
    Loan_to_Income: float

model, scaler = load_model_and_scaler("models/best_model.joblib", "models/scaler_standard.joblib")

@app.post("/predict")
def predict(inp: InputData):
    sample = {
        "Income": inp.Income,
        "Age": inp.Age,
        "Loan": inp.Loan,
        "Loan to Income": inp.Loan_to_Income
    }
    return predict_sample(sample, model, scaler)
