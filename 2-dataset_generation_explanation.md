# Dataset Generation & Feature Engineering Strategy

This document details how the final unified dataset (`financial_profiles.csv`) consisting of 110,000+ realistic user properties was constructed. 

## 1. The Challenge with "Joining" Kaggle Datasets
Initially, we had four distinct, completely independent datasets from Kaggle:
1. [credit_risk_dataset.csv](file:///c:/project-at/backend/data/raw/credit_risk_dataset.csv) (32,581 rows)
2. [financial_hci_dataset.csv](file:///c:/project-at/backend/data/raw/financial_hci_dataset.csv) (1,300 rows)
3. [german_credit_data.csv](file:///c:/project-at/backend/data/raw/german_credit_data.csv) (1,000 rows)
4. [marketing_campaign.csv](file:///c:/project-at/backend/data/raw/marketing_campaign.csv) (2,240 rows)

Because these datasets were collected independently by different organizations, they **do not share a common `User_ID`**. Therefore, performing a traditional SQL `JOIN` (e.g., matching User 1 in `credit_risk` to User 1 in `marketing`) is statistically invalid and would corrupt the data. 

**Our Solution:** 
Instead of forcing invalid joins, we used the largest schema—[credit_risk_dataset.csv](file:///c:/project-at/backend/data/raw/credit_risk_dataset.csv) (32k rows)—as the "Ground Truth Seed". We then used statistical synthesis and correlation logic to generate the missing columns required by our Neural Network, ensuring realistic financial behavior.

---

## 2. Step-by-Step Generation Pipeline

### Step 1: Bootstrapping to 110,000 Records
We took the 32,581 clean rows from [credit_risk_dataset.csv](file:///c:/project-at/backend/data/raw/credit_risk_dataset.csv) and ran a **Random Sampling with Replacement** algorithm until we produced 110,000 rows. This effectively upscaled our data pool.

### Step 2: Injecting Statistical Noise (Jitter)
To ensure the 110,000 rows aren't exact duplicates, we applied statistical variance to the base values:
- **`age`**: Original age + random variance between `-3` and `+4` years.
- **`monthly_income`**: Original annual income $\div 12$, augmented by $\pm 5\%$ variation.
- **`loan_amount`**: Original loan amount factored by $\pm 5\%$ variation.

### Step 3: Synthesizing Missing Operational Variables
Using realistic financial assumptions and correlations, we calculated the missing columns:
- **`monthly_expenses`**: Randomized between $30\%$ to $90\%$ of `monthly_income`.
- **`total_savings`**: The remaining discretionary income ($Income - Expenses$) multiplied by a randomized duration factor (to simulate months/years of accumulated savings).
- **`monthly_emi` (Equated Monthly Installment)**: Calculated using the standard Amortization Formula assuming a 4 year (48 month) term based on their specific interest rate (`loan_int_rate`).
  - *Formula:* $EMI = P \times r \times \frac{(1+r)^n}{(1+r)^n - 1}$
- **`credit_score`**: Heavily influenced by the `cb_person_default_on_file` column. If a user had a history of defaulting, their score was randomized in the "Poor" bracket (`300-580`). If clear, it was randomized in "Good/Excellent" (`600-850`).
- **`credit_card_usage`**: A random utilization parameter between $5\%$ and $95\%$.

### Step 4: Generating the Target Labels for Machine Learning
Finally, our Neural Network requires exactly 4 continuous/binary target variables to evaluate "Financial Stability". We mapped them programmatically:
1. **`savings_ratio`**: $\frac{Total Savings}{Annual Income}$
2. **`debt_ratio`**: $\frac{EMI + (Credit Card Usage \times 0.2 \times Monthly Income)}{Monthly Income}$
3. **`budget_stability`**: $1.0 - \frac{Monthly Expenses}{Monthly Income}$
4. **`risk_level`**: Directly inherited from the Kaggle target `loan_status` (0 = Safe, 1 = Defaulted/High Risk).

---

## 3. How the Transaction Tables Work with This
The [financial_hci_dataset.csv](file:///c:/project-at/backend/data/raw/financial_hci_dataset.csv) represents **Time-Series Transaction Logs**. 

When building our FastAPI application later, our data flow will represent an aggregate:
1. A **User** will have a baseline snapshot equivalent to exactly 1 row from `financial_profiles.csv` (this holds their profile and sets their *Risk Score*).
2. The **User** will track day-to-day spending over time. Inside the application, XGBoost and Isolation Forest will consume the transaction patterns from [financial_hci_dataset.csv](file:///c:/project-at/backend/data/raw/financial_hci_dataset.csv) to learn statistical anomalies (e.g. flagging a sudden $5,000 grocery bill). 

In short, the structured profiles train the **Neural Network**, and the raw transaction logs train the **Anomaly/Spending Predictors**.

Here is exactly how the correlation logic was applied in the code:

Monthly Expenses (Correlated to Income): People usually spend in proportion to what they earn. The script calculates expenses by taking the user's monthly_income and randomly multiplying it by a realistic utilization bracket (between 30% and 90%). This ensures a high-earner naturally spends more than a low-earner, keeping the ratios mathematically sound.
Total Savings (Correlated to Discretionary Income): We calculated discretionary ("leftover") income by simply doing 

(Income - Expenses)
. We then assumed the user had been saving this exact leftover amount for a random period between 5 and 60 months. This mathematically guarantees that a user who spends 90% of their paycheck will realistically have a tiny savings pool, while a frugal user has a large one.
Monthly EMI (Mathematically Exact): We didn't guess their monthly loan payment. Because the Kaggle dataset gave us their actual loan_amount and their loan_int_rate (interest rate), the script runs the literal, real-world Bank Amortization Formula for a 48-month loan: (Principal × Rate × (1 + Rate)⁴⁸ / (1 + Rate)⁴⁸ - 1). The resulting EMI is perfectly accurate for whatever loan they took out.
Credit Score (Correlated to Default History): The Kaggle dataset included a column called cb_person_default_on_file (which was either 'Y' or 'N'). If the real Kaggle data indicated the user had a history of defaulting, the script forced their synthesized credit score to fall specifically within the "Poor" bracket (300–580). If they had a clean record, it placed them in the "Good/Excellent" bracket (600–850).


Q: What features are there in the existing credit risk dataset? What are the others we added? A: The original 
credit_risk_dataset.csv
 contains baseline demographic and loan information. The key features we extracted from it were person_age, person_income, loan_amnt, loan_int_rate (interest rate), cb_person_default_on_file (history of defaulting), and loan_status (whether they defaulted on this specific loan, which we use directly as our risk_level target).

The features we synthesized (added) to make it a complete financial profile are:

monthly_expenses
total_savings
monthly_emi
credit_score
credit_card_usage
Target Labels: savings_ratio, debt_ratio, budget_stability
Q: Did we not consider the remaining datasets at all? Do we only train using the ones we generated? A: We use the generated financial_profiles.csv specifically to train the Risk Prediction Neural Network (because Neural Networks need massive amounts of structured profile data to learn baseline financial stability). However, we are still using the 
financial_hci_dataset.csv
! That dataset acts as our raw Transaction Ledger. It is used separately to train the Isolation Forest and XGBoost/Prophet models, which specialize in spotting time-series anomalies and forecasting daily spending habits independent of the user's statically generated profile.