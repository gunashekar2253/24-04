import pandas as pd
import numpy as np
import os

# Set seed for reproducibility
np.random.seed(42)

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed")

if not os.path.exists(PROCESSED_DIR):
    os.makedirs(PROCESSED_DIR)

print("Loading credit risk dataset...")
credit_df = pd.read_csv(os.path.join(RAW_DIR, "credit_risk_dataset.csv"))

print("Generating 100,000+ synthetic financial profiles...")
# Drop missing values to keep it clean
credit_df = credit_df.dropna(subset=['person_age', 'person_income', 'loan_amnt', 'loan_status'])

# We need 100,000+ records. We will sample 110,000 with replacement to ensure we hit 100k+ after any filtering.
TARGET_RECORDS = 110000
sampled_df = credit_df.sample(n=TARGET_RECORDS, replace=True).reset_index(drop=True)

# Add jitter/noise to base features to make them unique while preserving statistical relationships
age = np.clip(sampled_df['person_age'] + np.random.randint(-3, 4, size=TARGET_RECORDS), 18, 90)
# Add +/- 5% noise to income and loan amount
monthly_income = (sampled_df['person_income'] / 12) * np.random.uniform(0.95, 1.05, size=TARGET_RECORDS)
loan_amount = sampled_df['loan_amnt'] * np.random.uniform(0.95, 1.05, size=TARGET_RECORDS)

# Generate missing features logically based on the new noisy base features
monthly_expenses = monthly_income * np.random.uniform(0.3, 0.9, size=TARGET_RECORDS)
total_savings = np.maximum(0, (monthly_income - monthly_expenses) * np.random.uniform(5, 60, size=TARGET_RECORDS))

# Compute EMI
loan_int_rate = sampled_df['loan_int_rate'].fillna(10.0) # default 10%
monthly_int_rate = loan_int_rate / 100 / 12
loan_term_months = 48
# EMI formula: P * r * (1+r)^n / ((1+r)^n - 1)
emi = np.where(
    loan_amount > 0,
    loan_amount * monthly_int_rate * (1 + monthly_int_rate)**loan_term_months / ((1 + monthly_int_rate)**loan_term_months - 1),
    0
)

credit_score = np.where(
    sampled_df['cb_person_default_on_file'] == 'Y',
    np.random.randint(300, 580, size=TARGET_RECORDS),
    np.random.randint(600, 850, size=TARGET_RECORDS)
)

credit_card_usage = np.random.uniform(0.05, 0.95, size=TARGET_RECORDS)

# Compute targets
savings_ratio = np.clip(total_savings / (monthly_income * 12 + 1), 0, 1.0)
debt_ratio = np.clip((emi + credit_card_usage * (monthly_income * 0.2)) / (monthly_income + 1), 0, 1.0)
budget_stability = np.clip(1.0 - (monthly_expenses / (monthly_income + 1)), 0.0, 1.0)
risk_level = sampled_df['loan_status'] # 1 is default (high risk), 0 is non-default (low risk)

processed_df = pd.DataFrame({
    'age': age,
    'monthly_income': monthly_income,
    'monthly_expenses': monthly_expenses,
    'total_savings': total_savings,
    'loan_amount': loan_amount,
    'monthly_emi': emi,
    'credit_score': credit_score,
    'credit_card_usage': credit_card_usage,
    'savings_ratio': savings_ratio,
    'debt_ratio': debt_ratio,
    'budget_stability': budget_stability,
    'risk_level': risk_level
})

# Filter out unrealistic limits (e.g. age > 100)
processed_df = processed_df[processed_df['age'] <= 100]

output_path = os.path.join(PROCESSED_DIR, "financial_profiles.csv")
processed_df.to_csv(output_path, index=False)
print(f"Successfully generated {len(processed_df)} financial profiles and saved to {output_path}")

# Load transactions for sanity check
print("\nVerifying transactions dataset...")
transactions_df = pd.read_csv(os.path.join(RAW_DIR, "financial_hci_dataset.csv"))
print(f"Transactions dataset shape: {transactions_df.shape}")
print("Ready for ML Phase!")
