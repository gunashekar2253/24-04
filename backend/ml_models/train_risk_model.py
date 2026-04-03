import os
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "financial_profiles.csv")
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

print("Loading dataset for Risk Model...")
df = pd.read_csv(DATA_PATH)

features = ['age', 'monthly_income', 'monthly_expenses', 'total_savings', 
            'loan_amount', 'monthly_emi', 'credit_score', 'credit_card_usage']
X = df[features]
y = df['risk_level'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
print("Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, os.path.join(MODEL_DIR, "risk_scaler.pkl"))

# Build TensorFlow Model
print("Building and training Risk Prediction Model (ReLU-based)...")
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(len(features),)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation='sigmoid') # Binary classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train Model
history = model.fit(
    X_train_scaled, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Evaluate Model
loss, accuracy = model.evaluate(X_test_scaled, y_test)
print(f"Risk Model Test Accuracy: {accuracy:.4f}")

# Save Model
model_save_path = os.path.join(MODEL_DIR, "risk_model.h5")
model.save(model_save_path)
print(f"Risk Model saved successfully at {model_save_path}")
