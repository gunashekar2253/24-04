# AI Financial Decision System — Implementation Plan

Build a full-stack AI Financial Decision System with Flask backend, TensorFlow deep learning, and a polished dark-themed frontend matching the UI screenshots provided.

---

## Proposed Changes

### Component 1: Project Structure & Configuration

#### [NEW] [requirements.txt](file:///c:/project-at/requirements.txt)
- Flask, flask-login, flask-cors
- tensorflow, scikit-learn, pandas, numpy
- yfinance, matplotlib
- statsmodels (ARIMA)

#### [NEW] [config.py](file:///c:/project-at/config.py)
- App configuration (secret key, DB path, model paths)

---

### Component 2: Dataset Generation & Model Training

#### [NEW] [data/generate_dataset.py](file:///c:/project-at/data/generate_dataset.py)
- Generate 100,000+ financial profiles with realistic distributions
- Features: age, monthly_income, monthly_expenses, total_savings, loan_amount, monthly_emi, credit_score, credit_card_usage
- Labels: risk_level (Low/Medium/High), budget_stability, savings_ratio, debt_ratio
- Use realistic statistical distributions (income follows lognormal, credit scores follow beta distribution scaled to 300-850, etc.)
- Save to `data/financial_profiles.csv`

#### [NEW] [models/train_risk_model.py](file:///c:/project-at/models/train_risk_model.py)
- Load dataset, preprocess with StandardScaler
- Build TensorFlow/Keras neural network:
  - Input(8) → Dense(128, relu) → Dropout(0.3) → Dense(64, relu) → Dropout(0.2) → Dense(32, relu) → Output(3, softmax) for risk classification
  - Separate regression head for stability score
- Train with 80/20 split, early stopping
- Save model to `models/risk_model.h5` and scaler to `models/scaler.pkl`

#### [NEW] [models/train_anomaly_model.py](file:///c:/project-at/models/train_anomaly_model.py)
- Train Isolation Forest on spending patterns
- Save model to `models/anomaly_model.pkl`

---

### Component 3: Flask Backend API

#### [NEW] [app.py](file:///c:/project-at/app.py)
- Main Flask application entry point
- Initialize Flask app, database, login manager
- Register all route blueprints
- Run the server

#### [NEW] [database.py](file:///c:/project-at/database.py)
- SQLite database setup with tables: users, financial_profiles, transactions
- User CRUD operations
- Financial profile storage/retrieval

#### [NEW] [routes/auth.py](file:///c:/project-at/routes/auth.py)
- `/api/register` — user registration
- `/api/login` — user login
- `/api/logout` — user logout
- `/api/user` — get current user info

#### [NEW] [routes/profile.py](file:///c:/project-at/routes/profile.py)
- `/api/profile` — save/update financial profile
- `/api/profile/summary` — get profile with DL predictions
- `/api/profile/income` — save income details
- `/api/profile/expenses` — save expense categories

#### [NEW] [routes/analysis.py](file:///c:/project-at/routes/analysis.py)
- `/api/analysis/risk` — run risk prediction model
- `/api/analysis/anomalies` — run anomaly detection
- `/api/analysis/forecast` — run spending forecast
- `/api/analysis/optimize` — run budget optimization
- `/api/analysis/investment-capacity` — calculate safe investment amount

#### [NEW] [routes/query.py](file:///c:/project-at/routes/query.py)
- `/api/query` — classify user question and route to appropriate agent
- Query classification: financial_advice | budgeting | stock_query
- Financial Recommendation Agent logic
- Stock Analysis Agent routing

#### [NEW] [routes/stocks.py](file:///c:/project-at/routes/stocks.py)
- `/api/stocks/search` — search stock tickers
- `/api/stocks/analyze/<ticker>` — full stock analysis with yfinance
- `/api/stocks/insights/<ticker>` — profile-aware stock insights

---

### Component 4: AI/ML Engine Modules

#### [NEW] [engine/risk_predictor.py](file:///c:/project-at/engine/risk_predictor.py)
- Load trained TensorFlow model and scaler
- `predict_risk(profile_data)` → returns risk_level, stability_score, savings_ratio, debt_ratio

#### [NEW] [engine/anomaly_detector.py](file:///c:/project-at/engine/anomaly_detector.py)
- Isolation Forest + Z-score analysis
- `detect_anomalies(expenses)` → returns list of anomalous categories with explanations

#### [NEW] [engine/spending_forecaster.py](file:///c:/project-at/engine/spending_forecaster.py)
- ARIMA-based forecasting for next-month spending
- `forecast_spending(history)` → predicted amounts per category

#### [NEW] [engine/budget_optimizer.py](file:///c:/project-at/engine/budget_optimizer.py)
- Analyzes expense breakdown and suggests optimal cuts
- `optimize_budget(profile, expenses)` → list of recommendations with savings impact

#### [NEW] [engine/investment_calculator.py](file:///c:/project-at/engine/investment_calculator.py)
- Calculate safe investment capacity
- Factors: savings_ratio, debt_ratio, emergency buffer
- `calculate_investment_capacity(profile)` → safe monthly investment amount

#### [NEW] [engine/query_classifier.py](file:///c:/project-at/engine/query_classifier.py)
- Keyword-based + rule-based query classification
- Routes to financial_advice, budgeting, or stock_query

#### [NEW] [engine/stock_analyzer.py](file:///c:/project-at/engine/stock_analyzer.py)
- yfinance integration for real-time stock data
- `analyze_stock(ticker)` → price, P/E, volatility, trend, market cap
- `get_risk_matched_insights(ticker, risk_level)` → profile-aware commentary

---

### Component 5: Frontend (Dark-Themed Dashboard)

#### [NEW] [static/css/style.css](file:///c:/project-at/static/css/style.css)
- Dark theme matching the screenshots (deep navy/dark blue background)
- Card-based layout with subtle borders
- Gradient hero banner
- Responsive design

#### [NEW] [templates/login.html](file:///c:/project-at/templates/login.html)
- Login/Register tabbed form matching the screenshot
- Dark themed with centered card

#### [NEW] [templates/dashboard.html](file:///c:/project-at/templates/dashboard.html)
- Overview page with:
  - Welcome banner with user name, age, credit score, risk tolerance
  - Risk Level / Budget Stability / Savings Ratio / Debt Ratio cards
  - Quick Actions panel
  - Risk Assessment card
  - Income vs Expenses bar chart (Chart.js)
  - Expense Categories donut chart (Chart.js)
  - Recommendations section

#### [NEW] [templates/add_details.html](file:///c:/project-at/templates/add_details.html)
- Tabbed form: Income | Expenses
- Expense categories: Shopping, Food, Phone, Entertainment, Education, Beauty, Sports, Social, etc.

#### [NEW] [templates/query.html](file:///c:/project-at/templates/query.html)
- AI Query Assistant chatbot interface
- Chat bubble design matching screenshot

#### [NEW] [templates/stocks.html](file:///c:/project-at/templates/stocks.html)
- Stock search and analysis dashboard
- Key stats, tabs (Overview/Fundamentals/Valuation/News)
- AI Agent chat panel for stock-specific questions

#### [NEW] [static/js/app.js](file:///c:/project-at/static/js/app.js)
- API calls, Chart.js chart rendering
- Navigation, form handling, chat functionality

---

## Verification Plan

### Automated Tests
1. **Dataset generation**: Run `python data/generate_dataset.py` → verify CSV has 100,000+ rows with all columns
2. **Model training**: Run `python models/train_risk_model.py` → verify model files are saved and accuracy > 70%
3. **API endpoints**: Run server with `python app.py`, then use curl/browser to test each endpoint

### Browser Verification
1. Start the app with `python app.py`
2. Open browser to `http://localhost:5000`
3. Register a new user → verify login/register page matches dark theme
4. Add financial details → verify form works
5. View Overview dashboard → verify all 4 metric cards, charts render
6. Use AI Query Assistant → verify query classification and responses
7. Use Stock Analysis → verify yfinance data loads with ticker search

### Manual Verification
- Compare the running app UI against the provided screenshots to ensure visual fidelity
