# Phase 3 Summary: Model Training 🧠

## 📍 What is it?
The **Model Training** phase was the implementation of the "Intelligence Layer." We trained and saved multiple specialized AI models to handle different analytical tasks, from risk assessment to spending forecasts.

## 🚀 How we achieved it
We developed and executed a training pipeline for four distinct AI engines:
1.  **Risk Predictor (Deep Learning)**: A Neural Network with ReLU activation layers trained on the 110k profiles from Phase 2. It learns to classify a user as Low, Medium, or High risk.
2.  **Anomaly Detectors (Hybrid)**: A combination of a statistical **Isolation Forest** and a deep learning **Autoencoder** to flag "unusual" spending patterns (e.g., a $2,000 grocery bill).
3.  **Spending Forecaster (Time-Series)**: Used **XGBoost** (Gradient Boosting) and **Facebook Prophet** to learn seasonal spending habits and predict future monthly expenses.
4.  **Artifact Persistence**: Every model was saved as binary files (`.h5`, `.pkl`, `.json`) along with data scalers to ensure they could be loaded instantly by the FastAPI backend.

## 🛠️ What we used
- **TensorFlow / Keras**: For building the Risk Neural Network and Anomaly Autoencoder.
- **Scikit-learn**: For the Isolation Forest model and data preprocessing (StandardScaler).
- **XGBoost**: For high-accuracy gradient boosted regression in spending forecasts.
- **Facebook Prophet**: For additive modeling of time-series effects (holidays, weekends).

## 💡 Why we used it
- **Multi-Model Strategy**: One AI model can't do everything. We used TensorFlow for *classification*, Isolation Forest for *anomaly detection*, and Prophet for *time-series*, ensuring the best tool for each specific job.
- **ReLU Activation**: Used in the Neural Network to handle non-linear financial patterns effectively while maintaining computational efficiency.
- **Scalers (StandardScaler)**: We saved these alongside the models so that user inputs (like a $50,000 income) are normalized exactly like the training data, preventing "garbage-in-garbage-out."
- **Persistence**: Saving models as binaries allows the backend to perform "inference" (predictions) in milliseconds without retraining.
