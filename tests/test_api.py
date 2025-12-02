# tests/test_api.py
from fastapi.testclient import TestClient
from deployment.app import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data and data["status"] == "ok"

def test_predict_ok():
    sample = {"Income": 50000, "Age": 35, "Loan": 4000, "Loan_to_Income": 0.08}
    r = client.post("/predict", json=sample)
    assert r.status_code == 200
    j = r.json()
    assert "probability_of_default" in j and "predicted_label" in j
    assert isinstance(j["probability_of_default"], float)
    assert j["predicted_label"] in (0, 1)
