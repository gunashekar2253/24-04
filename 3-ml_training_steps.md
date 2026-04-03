# Phase 3: Machine Learning Model Training 🚀

Now that we have successfully generated the `110,000+` financial profiles and we have the raw time-series transaction dataset, we can train the **Brain** of the AI Financial Engine.

Here is the exact step-by-step roadmap to achieve Phase 3:

## Step 1: Install Deep Learning Dependencies
Because local AI models require heavy mathematical frameworks, our very first step is continuing the background installation of the core engines:
- **`tensorflow`** (For the Risk Neural Network and Anomaly Autoencoder)
- **`xgboost`** & **`prophet`** (For Time-Series Spending Forecasts)
- **`scikit-learn`** (For the Isolation Forest algorithm)

*Command: `.\venv\Scripts\pip.exe install -r requirements.txt`*

---

## Step 2: Train the Risk Predictor (TensorFlow ReLU)
Once TensorFlow is installed, we run [train_risk_model.py](file:///c:/project-at/backend/ml_models/train_risk_model.py).
**Inputs:** The 110k+ rows from `financial_profiles.csv` (Age, Income, Expenses, Savings, EMI, Credit Score).
**Outputs:** The model learns a baseline "Financial Stability" mapping and saves two artifacts to the `backend/ml_models/` folder:
1. `risk_scaler.pkl` (Used to scale live user data in the FastAPI app)
2. `risk_model.h5` (The compiled Neural Network binary)

---

## Step 3: Train the Anomaly Detector (Isolation Forest + Autoencoder)
Next, we run `train_anomaly_model.py` targeting the raw transaction ledger (`financial_hci_dataset.csv`).
**Inputs:** Transaction Amounts and Balances.
**Outputs:** The script trains both a statistical and deep-learning anomaly engine. It saves:
1. `anomaly_scaler.pkl`
2. `isolation_forest.pkl`
3. `autoencoder.h5`

---

## Step 4: Train the Spending Forecaster (XGBoost + Prophet)
Finally, we execute `train_spending_model.py` on the historical timeline of the transactions.
**Inputs:** Chronological Dates (`ds`) and Spent Amounts (`y`).
**Outputs:** The models learn the seasonal habits of users (e.g. they spend more on weekends). It saves:
1. `spending_xgboost.pkl`
2. `spending_prophet.json`

---

## Step 5: Verification
At the end of this Phase, our `backend/ml_models/` directory will be successfully populated with all six compiled intelligence binaries. The Backend engine will finally be ready to integrate them!
