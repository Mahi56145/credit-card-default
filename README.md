# Credit Card Default Prediction  
**Author:** Mahipal Mali  
**Tools:** Python, Scikit-Learn, Pandas, Matplotlib, Seaborn  

This project predicts whether a credit card customer will default on their loan using machine learning.  
The workflow includes: data understanding, exploratory data analysis (EDA), preprocessing, model training, evaluation, and inference.

---

## 📌 Project Overview
- **Goal:** Predict customer default (0 = No Default, 1 = Default)
- **Dataset size:** 2,000 rows × 5 columns  
- **Features:**
  - Income  
  - Age  
  - Loan  
  - Loan to Income Ratio  
  - Default (Target)

---

## 📊 EDA Highlights
- No missing values  
- Balanced preprocessing  
- Strong correlation of *Loan to Income* with *Default*  
- Visualizations include:
  - Histograms  
  - Boxplots  
  - Correlation heatmap  
  - Confusion matrices  
  - ROC curves  

---

## ⚙️ Preprocessing Steps
- Train–test split (80/20, stratified)  
- Standard scaling of numeric features  
- Saving processed datasets:
  - `data/processed/train_processed.csv`
  - `data/processed/test_processed.csv`
- Saving scaler:  
  `models/scaler_standard.joblib`

---

## 🤖 Models Trained
Two machine learning models were trained:

1. **Logistic Regression**
2. **Random Forest Classifier**

**Selected Best Model:** Random Forest  
**Best ROC-AUC:** 1.0000

All models are saved in `/models`.

---

## 🧪 Evaluation Metrics
Metrics used:

- Accuracy  
- Precision  
- Recall  
- F1-Score  
- ROC-AUC  

Random Forest achieved perfect scores on the test set.

---

## 🚀 Inference Example

```python
import pandas as pd
import joblib

# load scaler + best model
scaler = joblib.load("models/scaler_standard.joblib")
model = joblib.load("models/best_model.joblib")

sample = {
    "Income": 50000,
    "Age": 35,
    "Loan": 4000,
    "Loan to Income": 0.08
}

df = pd.DataFrame([sample])
scaled = scaler.transform(df)
pred = model.predict(scaled)[0]
proba = model.predict_proba(scaled)[0][1]

print("Prediction:", pred)
print("Probability of default:", proba)
