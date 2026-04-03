# AI Financial Decision System — Questions & Answers

---

## Q1: Users should first fill the details like salary etc?

**Yes, exactly.** When a user registers and logs in for the first time, they are taken to the **"Add Details"** page where they must fill in their financial profile before accessing the dashboard.

### What they fill on first login:

| Field | Example |
|-------|---------|
| Currency Type | INR (₹) or USD ($) |
| Age | 30 |
| Monthly Income / Salary | ₹50,000 |
| Monthly Expenses | ₹30,000 |
| Total Savings | ₹2,00,000 |
| Loan Amount | ₹5,00,000 |
| Monthly EMI | ₹8,000 |
| Credit Score | 720 |
| Credit Card Usage (%) | 40% |

### Flow:
```
Register → Login → Fill Financial Profile (mandatory) → Dashboard unlocks
```

Until the user completes this profile, the Overview dashboard will show a prompt: **"Please complete your financial profile to see your analysis."**

---

## Q2: Users should daily enter their expenditures?

**Yes.** The system has two types of data entry:

### One-Time Setup (Profile):
- Salary, savings, loan, EMI, credit score — filled once, updated when things change

### Daily / Regular Transactions:
- Users add individual transactions through the **"+ Add New"** button on the Overview page or the **"Add Details"** page
- Each transaction has: **Date, Category, Description, Type (Income/Expense), Amount**

### Example daily entries:
| Date | Category | Type | Amount |
|------|----------|------|--------|
| 02 Apr 2026 | Food | Expense | ₹500 |
| 02 Apr 2026 | Transport | Expense | ₹150 |
| 01 Apr 2026 | Bonus | Income | ₹10,000 |

### Why daily entry matters:
- The **Anomaly Detection** engine needs real spending data to flag unusual expenses
- The **Spending Forecast** model (LSTM/ARIMA) learns from the user's transaction history to predict future spending
- The **Budget Optimizer** uses actual spending patterns to suggest where to cut
- **More data = better predictions** — the system gets smarter over time

---

## Q3: Where can I get the data for training?

The training dataset combines **real-world datasets from Kaggle** + **synthetic augmentation** to reach 1 lakh+ (100,000+) records.

### Real Datasets (Kaggle / Public Sources):

| Dataset | What it provides | Link |
|---------|-----------------|------|
| **German Credit Data (UCI)** | Credit risk labels, income, loan amounts, credit history | [Kaggle](https://www.kaggle.com/datasets/uciml/german-credit) |
| **Credit Card Customers** | Credit limit, usage ratio, income, spending patterns | [Kaggle](https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers) |
| **Lending Club Loan Data** | Loan amount, EMI, income, debt-to-income ratio, risk grade | [Kaggle](https://www.kaggle.com/datasets/wordsforthewise/lending-club) |
| **Home Credit Default Risk** | Income, credit amount, age, employment, loan default labels | [Kaggle](https://www.kaggle.com/c/home-credit-default-risk) |
| **Consumer Expenditure Survey (India/US)** | Category-level spending patterns by demographics | Government open data portals |
| **Adult Income Dataset (UCI)** | Age, income brackets, work class | [Kaggle](https://www.kaggle.com/datasets/uciml/adult-census-income) |

### How we build the 1 lakh+ dataset:

```
Step 1: Download 2-3 real datasets from above (gives ~30,000-50,000 real records)
Step 2: Map columns to our required features (age, income, expenses, savings, loan, EMI, credit_score, cc_usage)
Step 3: Generate synthetic data (~50,000-70,000 records) using realistic statistical distributions
Step 4: Combine real + synthetic → 1,00,000+ total records
Step 5: Calculate labels → risk_level, budget_stability, savings_ratio, debt_ratio
```

### Synthetic data generation uses:
- **Income**: Lognormal distribution (realistic right-skewed incomes)
- **Credit Score**: Beta distribution scaled to 300–850 range
- **Expenses**: Based on income with random category proportions
- **Loans/EMI**: Correlated with income level and age

---

## Q4: Should there be an option to edit details like increase in salary, new loan, etc?

**Absolutely yes.** The system includes an **"Update Profile"** feature in the Quick Actions panel.

### What can be edited:

| Field | Example Change |
|-------|---------------|
| Monthly Salary | Got a raise: ₹50,000 → ₹65,000 |
| Loan Amount | Took a new home loan: ₹0 → ₹20,00,000 |
| Monthly EMI | New EMI started: ₹0 → ₹15,000 |
| Credit Score | Score improved: 650 → 720 |
| Total Savings | Updated savings: ₹2,00,000 → ₹3,50,000 |
| Credit Card Usage | Reduced usage: 60% → 35% |

### What happens after editing:
```
User updates salary → System re-runs the deep learning model →
    Risk Level recalculated
    Budget Stability updated
    Savings Ratio updated
    Debt Ratio updated
    Budget Optimization refreshed
    Investment Capacity recalculated
    All dashboard cards update instantly
```

### Change history:
The system stores a **history log** so it can track how the user's financial profile has improved or worsened over time (useful for trend analysis).

---

## Q5: What are we training the model for — analyzing or giving answers from the bot?

**Both, but they are separate models serving different purposes:**

### Model 1: Deep Learning Risk Prediction Model (TensorFlow)
- **Purpose**: Analyzing the user's financial health
- **Input**: 8 financial features (age, income, expenses, savings, loan, EMI, credit_score, cc_usage)
- **Output**: Risk Level (Low/Medium/High), Budget Stability Score (0-100), Savings Ratio, Debt Ratio

```
Training Data (1 lakh records) → TensorFlow Neural Network → Saved Model (.h5)

When user fills profile → Model predicts → Dashboard shows results
```

### Model 2: Anomaly Detection Model (Isolation Forest)
- **Purpose**: Detecting unusual spending behavior
- **Input**: Category-level spending data from transactions
- **Output**: "Anomaly detected — food spending increased 125% compared to normal"

### Model 3: Spending Forecast Model (ARIMA/LSTM)
- **Purpose**: Predicting future expenses
- **Input**: User's transaction history over time
- **Output**: "Next month estimated spending: ₹3,200"

### The AI Bot (Query Assistant) — NOT a trained model
- The bot **does NOT use its own trained model**
- It uses **rule-based query classification** (keywords like "stock", "budget", "save", "invest")
- It **routes queries to the right engine**:
  - Financial question → calls Risk Model + Budget Optimizer → generates text response
  - Stock question → calls yfinance API + Stock Analyzer → generates stock insights

```
User asks "How can I reduce expenses?"
    → Query classified as "budgeting"
    → Bot calls Budget Optimizer engine
    → Engine analyzes user's expense categories
    → Bot responds: "Reduce shopping by 10% to save ₹3,000/month"
```

### Summary:

| Component | What it does | How |
|-----------|-------------|-----|
| **Risk Model** | Analyzes financial health | TensorFlow (trained on 1L dataset) |
| **Anomaly Model** | Detects unusual spending | Isolation Forest (trained on spending patterns) |
| **Forecast Model** | Predicts future spending | ARIMA on transaction history |
| **AI Bot** | Answers questions | Rule-based routing → calls the models above |

---

## Q6: Since we buy a stock, will the dashboard update based on the stock value and give suggestions?

**Important clarification: This system does NOT allow users to buy stocks.** It only provides **stock analysis and insights**.

### What the Stock Analysis page does:

```
User searches "TCS" → System fetches LIVE data from yfinance API →
    Shows: Price, Change, Market Cap, Volume, P/E Ratio, Volatility
    Shows: AI Confidence score (based on trend analysis)
    Shows: Profile-aware insight (matches stock risk to user's risk level)
```

### Profile-Aware Insights (How it connects to the user's financial data):

| User's Risk Level | Stock Volatility | System Says |
|-------------------|-----------------|-------------|
| LOW Risk | High Volatility Stock | ⚠️ "This stock's volatility is too high for your risk profile. Consider safer alternatives." |
| LOW Risk | Low Volatility Stock | ✅ "This stock aligns well with your conservative risk profile." |
| MEDIUM Risk | Medium Volatility Stock | ✅ "Balanced growth stock suitable for your risk tolerance." |
| HIGH Risk | High Volatility Stock | ℹ️ "You can handle higher risk, but limit exposure to max 20% of investment capacity." |

### Investment Capacity Connection:

```
Dashboard shows: Investment Capacity = ₹800/month
User looks at a stock priced at ₹2,358

System shows: "Based on your safe investment capacity of ₹800/month,
you could accumulate enough for 1 share in ~3 months through a SIP approach."
```

### What the system does NOT do:
- ❌ Does NOT execute stock purchases
- ❌ Does NOT track a stock portfolio
- ❌ Does NOT show profit/loss from holdings
- ❌ Does NOT give direct "BUY" or "SELL" recommendations

### What the system DOES do:
- ✅ Shows live stock data (price, volatility, P/E ratio, trend)
- ✅ Analyzes whether a stock matches the user's risk profile
- ✅ Shows how much the user can safely invest per month
- ✅ Provides educational insights about stock characteristics
- ✅ AI Agent answers questions about specific stocks

### Why no buy/sell?
This is a **financial decision support system**, not a trading platform. Adding actual trading would require SEBI/SEC compliance, brokerage APIs, and legal regulatory requirements — which is beyond the scope of this project.
