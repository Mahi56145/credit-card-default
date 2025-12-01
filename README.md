# Credit Card Default Prediction  
Author: Mahipal Mali  

This project predicts whether a customer will default on a credit card payment using Logistic Regression and Random Forest.  
The repository follows a modular, industry-style ML project structure.

---

## 📁 Project Structure
.
├── data/
│ ├── raw/ # raw dataset (if added later)
│ └── processed/ # train_processed.csv, test_processed.csv
├── models/ # saved ML models + scaler
├── notebooks/
│ └── credit_card_default_final.ipynb
├── src/
│ ├── data_loader.py # handles dataset loading
│ ├── preprocessing.py # scaling, splitting, transformations
│ ├── train.py # model training code
│ └── predict.py # inference pipeline
├── tests/
│ └── test_basic.py # unit tests
├── deployment/
│ └── app.py # future Flask/FastAPI app file
├── requirements.txt
├── README.md
└── .gitignore

---

## 🚀 How to Run

### 1️⃣ Install dependencies
pip install -r requirements.txt

### 2️⃣ Run training (models saved inside `/models`)
python src/train.py

### 3️⃣ Run inference
python src/predict.py

---

## 📊 Models Trained
- Logistic Regression  
- Random Forest (Best model – highest ROC AUC = 1.00)

Saved models:
models/
├── logisticregression.joblib
├── randomforest.joblib
├── best_model.joblib
└── scaler_standard.joblib

---

## 🧪 Tests
Run basic unit test:
pytest

---

## 📄 Notebook for Evaluation
Notebook used for model development:

notebooks/credit_card_default_final.ipynb

---

## 📌 Next Improvements
- Hyperparameter tuning  
- SHAP explainability  
- Deploy using FastAPI or Flask  
- CI/CD pipeline  
