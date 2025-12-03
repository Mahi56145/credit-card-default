Credit Card Default Prediction — ML Web App (FastAPI + React)

This project is a complete machine-learning web application that predicts whether a person is likely to default on a credit card loan.

✔ Backend: FastAPI (Python)
✔ Frontend: React + Tailwind (bundled inside ui/dist/)
✔ Model: Random Forest (trained using scikit-learn)
✔ Deployment: Render (Free Tier)

🚀 Live Demo
API Root:

🔗 https://creditcardprediction-cxhb.onrender.com

Full Web UI:

🔗 https://creditcardprediction-cxhb.onrender.com/ui

API Docs (Swagger):

🔗 https://creditcardprediction-cxhb.onrender.com/docs

📁 Project Structure
credit-card-default/
│
├── deployment/
│   ├── app.py                 # FastAPI backend
│   └── ...                    
│
├── models/
│   ├── best_model.joblib
│   ├── scaler_standard.joblib
│
├── ui/
│   ├── dist/                  # Production-ready frontend bundle
│   │   ├── index.html
│   │   └── assets/
│   └── src/                   # React source (optional)
│
├── data/                      # Raw + processed datasets
│
├── requirements.txt
└── README.md

⚙️ Backend Endpoint Summary
GET /

Returns UI if available

Otherwise simple JSON response

GET /ui

Loads the React UI from ui/dist/index.html.

POST /predict

Predict default probability.

Example request:
{
  "Income": 50000,
  "Age": 35,
  "Loan": 4000,
  "Loan_to_Income": 89
}

Example response:
{
  "probability_of_default": 0.29,
  "predicted_label": 0
}

🧠 How the Model Works

StandardScaler normalizes the input features

RandomForestClassifier predicts probability of default

Pretrained .joblib files are loaded lazily (only when needed)

ML Files:

models/best_model.joblib

models/scaler_standard.joblib

🔧 Local Development
1. Create environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

2. Install dependencies
pip install -r requirements.txt

3. Run FastAPI locally
uvicorn deployment.app:app --reload


Local URLs:

UI → http://127.0.0.1:8000/ui

API Docs → http://127.0.0.1:8000/docs

☁️ Deploying on Render (Without Docker)
1. Connect GitHub Repo

Render → New Web Service → Select your repository.

2. Configure Build Settings
Setting	Value
Runtime	Python
Build Command	pip install -r requirements.txt
Start Command	gunicorn deployment.app:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 1 --timeout 120
3. Make sure UI is built

Render expects:

ui/dist/index.html
ui/dist/assets/*


If not built:

cd ui
npm install
npm run build


Then commit and push.

Render automatically redeploys.

🧪 Testing the API via cURL
curl -X POST "https://creditcardprediction-cxhb.onrender.com/predict" \
     -H "Content-Type: application/json" \
     -d '{"Income":50000,"Age":35,"Loan":4000,"Loan_to_Income":89}'
⚠️ Notes & Common Issues
UI not showing on /. Only JSON appears

Make sure:

ui/dist/index.html


exists AND is committed to GitHub.

Worker Timeout / Out of Memory

Use 1 worker on Render free tier

Lazy loading model (already configured) prevents boot timeout

404 on /static or /ui

Means ui/dist/ is missing or incorrectly built.

🙌 Credits

Created by Mahipal (Mahi)
Built with:

Python, FastAPI, scikit-learn

React, TailwindCSS

Render Cloud Hosting