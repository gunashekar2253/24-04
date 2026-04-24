import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "financial_profiles.csv")
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

print("Loading dataset for Risk Model (Deep Learning)...")
df = pd.read_csv(DATA_PATH)

# -----------------------------
# Feature Engineering (same)
# -----------------------------
df['expense_ratio'] = df['monthly_expenses'] / df['monthly_income'].replace(0, 1)
df['debt_ratio'] = df['loan_amount'] / (df['monthly_income'] * 12).replace(0, 1)

features = [
    'age', 'monthly_income', 'monthly_expenses', 'total_savings',
    'loan_amount', 'monthly_emi', 'credit_score', 'credit_card_usage',
    'expense_ratio', 'debt_ratio'
]

X = df[features]
y = df['risk_level']   # assume 0,1,2 classes

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Scaling (same as your code)
# -----------------------------
print("Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, os.path.join(MODEL_DIR, "risk_scaler.pkl"))

# -----------------------------
# Convert labels (for NN)
# -----------------------------
num_classes = len(np.unique(y))
y_train_cat = to_categorical(y_train, num_classes)
y_test_cat = to_categorical(y_test, num_classes)

# -----------------------------
# Build Neural Network (ReLU)
# -----------------------------
print("Building Deep Learning Model...")

model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(num_classes, activation='softmax')   # classification
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# -----------------------------
# Train Model
# -----------------------------
print("Training model...")
model.fit(
    X_train_scaled,
    y_train_cat,
    epochs=30,
    batch_size=16,
    validation_split=0.1,
    verbose=1
)

# -----------------------------
# Evaluate
# -----------------------------
print("Evaluating model...")
loss, acc = model.evaluate(X_test_scaled, y_test_cat)
print(f"Deep Learning Test Accuracy: {acc:.4f}")

# -----------------------------
# Save Model
# -----------------------------
model_path = os.path.join(MODEL_DIR, "risk_model_nn.h5")
model.save(model_path)

print(f"Deep Learning Model saved at {model_path}")