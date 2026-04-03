# Phase 2: Dataset Requirements & Kaggle Integration

To train robust, real-world Machine Learning models for the AI Financial Decision System, we need to transition from purely synthetic data to combining **real-world Kaggle datasets** with logical augmentation.

This document outlines exactly what data we need, where to find it on Kaggle, and how we will process it.

---

## 1. The Core Objective

Our system relies on 3 main ML tasks:
1. **Risk Prediction**: Categorizing a user's financial health and calculating stability scores.
2. **Spending Forecast**: Predicting future spending based on time-series behavior.
3. **Anomaly Detection**: Flagging unusual spending behavior.

To power these, we need two distinct types of datasets:
1. **Cross-Sectional User Profile Data** (for the Risk Predictor)
2. **Time-Series Transaction Data** (for Spending Forecast and Anomalies)

---

## 2. Requirement A: User Profile Dataset (For Risk Model)

We need a dataset representing thousands of individual users and their financial snapshot at a given time.

### **Required Columns (Features)**
Our neural network expects exactly these 8 inputs. If a Kaggle dataset misses one, we must synthesize it based on the other variables using statistical correlation.

1. `age` (Years: 18 - 80)
2. `monthly_income` (Total inbound money per month)
3. `monthly_expenses` (Total outbound money per month)
4. `total_savings` (Liquid cash / bank balance)
5. `loan_amount` (Total outstanding debt)
6. `monthly_emi` (Fixed monthly debt payments)
7. `credit_score` (FICO equivalent: 300 - 850)
8. `credit_card_usage` (Utilization ratio: 0% - 100%)

### **Target Labels (Ground Truth to be generated)**
Kaggle datasets rarely have our exact custom "Risk Level" labels. We will calculate these programmatically from the 8 features above to act as the Ground Truth for the Neural Network:
- `savings_ratio` = [(total_savings / monthly_income) * 100](file:///c:/project-at/backend/app/models/user.py#6-20)
- `debt_ratio` = [(monthly_emi / monthly_income) * 100](file:///c:/project-at/backend/app/models/user.py#6-20)
- `budget_stability` = Algorithm combining Debt, Savings, and Credit Score (0-100)
- `risk_level` = Low (Stability > 75), Medium (40-75), High (< 40)

### **Recommended Kaggle Sources**
1. **[Credit Risk Dataset](https://www.kaggle.com/datasets/laotse/credit-risk-dataset)**
   - *Has*: Age, Income, Loan Amount, Loan Intent.
   - *Missing*: Credit Score, Savings. We would generate Credit Score inversely correlated to loan default status.
2. **[Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)**
   - *Has*: Income, Demographics, Spending habits.
3. **[German Credit Data](https://www.kaggle.com/datasets/uciml/german-credit)**
   - Excellent for mapping credit behavior to personal profiles.

---

## 3. Requirement B: Transaction Dataset (For Forecast & Anomalies)

To train Time-Series Forecasting (Prophet/XGBoost) and Anomaly Detection (Isolation Forest/Autoencoder), we need chronological data.

### **Required Columns (Features)**
1. `user_id` (To group transactions chronologically per user)
2. `transaction_date` (Daily/Weekly granular)
3. `category` (e.g., Food, Transport, Shopping, Utilities, Salary)
4. `amount` (Transaction numerical value)
5. `type` (`income` or `expense`)

### **What the Models Learn:**
- **Prophet/XGBoost**: Learns that a user who makes $60k/year typically spends $400 on Groceries in Week 1 of the month.
- **Isolation Forest**: Learns that a $2,500 "Shopping" expense from a user who averages $150 is a statistical anomaly.

### **Recommended Kaggle Sources**
1. **[Bank Transaction Data](https://www.kaggle.com/datasets/apoorvrp/bank-transaction-data)**
   - Real, anonymized bank transactions with exact dates and amounts. Perfect for time-series.
2. **[Personal Finance Dataset](https://www.kaggle.com/datasets/jasonpinnick/personal-finance-dataset)**
   - Categorized daily spending (Food, Bills, Shopping).

---

## 4. The Execution Plan for Phase 2

Since no single Kaggle dataset perfectly matches our specific 8-input API structure, the pipeline for Phase 2 (the `generate_dataset.py` script) will look like this:

### **Step 1: Download & Ingest**
- Download the chosen Kaggle datasets locally to `backend/data/raw/`.

### **Step 2: Cleaning & Feature Mapping**
- Rename Kaggle columns to match our database (e.g., `ApplicantIncome` → `monthly_income`).
- Drop irrelevant columns (e.g., zip code, marital status).
- Normalize currencies (if the dataset is in USD, multiply by 83 to create INR variations).

### **Step 3: Imputation (Smart Synthesis)**
- If a Kaggle dataset has `income` and `loan_amount` but is missing `monthly_emi`, we calculate a simulated EMI using a standard 12% interest rate formula.
- If `credit_score` is missing, we synthesize it using a bounded normal distribution biased by their `loan_status` (Default = 500s, Paid = 750s).

### **Step 4: Target Calculation**
- Calculate our math-based Ground Truths (`risk_level`, `budget_stability`, `savings_ratio`, `debt_ratio`) row by row.

### **Step 5: Output**
- Save the final massive dataset to `backend/data/financial_profiles.csv`.
- This CSV will now contain 100,000+ realistic, Kaggle-backed records perfectly formatted to train our specific neural networks.
