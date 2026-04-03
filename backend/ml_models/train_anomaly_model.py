import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "financial_hci_dataset.csv") # Transactions
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

print("Loading transactions dataset for Anomaly Detection...")
df = pd.read_csv(DATA_PATH)

# Feature engineering for anomaly detection
# We will use Amount and potentially encode Category
features = ['Amount'] # Adding more features if available, like Balance_After_Transaction
if 'Balance_After_Transaction' in df.columns:
    features.append('Balance_After_Transaction')

X = df[features].fillna(0)

# Scale features
print("Scaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save scaler
joblib.dump(scaler, os.path.join(MODEL_DIR, "anomaly_scaler.pkl"))

# 1. Train Isolation Forest
print("Training Isolation Forest...")
iso_forest = IsolationForest(contamination=0.05, random_state=42)
iso_forest.fit(X_scaled)

# Save Isolation Forest
iso_model_path = os.path.join(MODEL_DIR, "isolation_forest.pkl")
joblib.dump(iso_forest, iso_model_path)
print(f"Isolation Forest saved successfully at {iso_model_path}")

# 2. Train Autoencoder (TensorFlow)
print("Training Autoencoder for Anomaly Detection...")
input_dim = X_scaled.shape[1]

# Define Autoencoder
autoencoder = tf.keras.Sequential([
    # Encoder
    tf.keras.layers.Dense(8, activation="relu", input_shape=(input_dim,)),
    tf.keras.layers.Dense(4, activation="relu"),
    # Decoder
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(input_dim, activation="linear")
])

autoencoder.compile(optimizer='adam', loss='mse')

# Train Autoencoder
history = autoencoder.fit(
    X_scaled, X_scaled,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Save Autoencoder
auto_model_path = os.path.join(MODEL_DIR, "autoencoder.h5")
autoencoder.save(auto_model_path)
print(f"Autoencoder saved successfully at {auto_model_path}")
