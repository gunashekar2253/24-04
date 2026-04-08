# AI Financial Decision System — Task List

## Phase 1: Project Setup
- [x] Create project directory structure (backend/ + frontend/)
- [x] Create [backend/requirements.txt](file:///c:/project-at/backend/requirements.txt)
- [x] Create [backend/.env](file:///c:/project-at/backend/.env) (JWT secret + Gemini API key)
- [x] Create [backend/app/config.py](file:///c:/project-at/backend/app/config.py)
- [x] Initialize React app with Vite (`frontend/`)
- [x] Install all dependencies

## Phase 2: Dataset & Model Training
- [x] Create `backend/data/generate_dataset.py` — 100K+ profiles
- [x] Generate the dataset CSV
- [x] Create [backend/ml_models/train_risk_model.py](file:///c:/project-at/backend/ml_models/train_risk_model.py) — TensorFlow (ReLU)
- [x] Train risk prediction model
- [x] Create [backend/ml_models/train_anomaly_model.py](file:///c:/project-at/backend/ml_models/train_anomaly_model.py) — Isolation Forest + Autoencoder
- [x] Train anomaly detection models
- [x] Create [backend/ml_models/train_spending_model.py](file:///c:/project-at/backend/ml_models/train_spending_model.py) — XGBoost + Prophet
- [x] Train spending prediction models

## Phase 3: Backend — Database & Auth
- [x] Create [backend/app/database.py](file:///c:/project-at/backend/app/database.py) — SQLAlchemy + SQLite3
- [x] Create `backend/app/models/` — User, Profile, Transaction, Goal
- [x] Create `backend/app/schemas/` — Pydantic schemas
- [x] Create `backend/app/routes/auth.py` — JWT register/login
- [x] Create `backend/app/main.py` — FastAPI entry point

## Phase 4: Backend — AI/ML Engine Modules
- [x] Create `engine/risk_predictor.py` — TensorFlow risk prediction
- [x] Create `engine/anomaly_detector.py` — Isolation Forest + Autoencoder
- [x] Create `engine/spending_forecaster.py` — XGBoost + Prophet
- [x] Create `engine/budget_optimizer.py` — budget optimization
- [x] Create `engine/investment_calculator.py` — safe investment capacity
- [x] Create `engine/query_classifier.py` — finance-only filter
- [x] Create `engine/gemini_chat.py` — direct Gemini API (finance-only)
- [x] Create `engine/goal_planner.py` — goal-based planning
- [x] Create `engine/stock_agent.py` — CrewAI + yfinance

## Phase 5: Backend — API Routes
- [x] Create `routes/profile.py` — profile CRUD
- [x] Create `routes/transactions.py` — transaction CRUD
- [x] Create `routes/analysis.py` — dashboard data (works without transactions)
- [x] Create `routes/query.py` — Gemini finance-only chat (no stock)
- [x] Create `routes/goals.py` — goal CRUD + AI plans
- [x] Create `routes/stocks.py` — CrewAI stock agent + stock chat

## Phase 6: React.js Frontend
- [x] Create `src/context/AuthContext.jsx` — JWT auth
- [x] Create `src/services/api.js` — Axios + JWT
- [x] Create `src/index.css` — dark theme design system
- [x] Create `src/App.jsx` — routing
- [x] Create `src/components/Navbar.jsx`
- [x] Create `src/pages/Login.jsx` — login/register
- [x] Create `src/pages/Dashboard.jsx` — overview (works without transactions)
- [x] Create `src/pages/AddDetails.jsx` — transaction entry
- [x] Create `src/pages/AIAssistant.jsx` — Gemini finance chat
- [x] Create `src/pages/StockAnalysis.jsx` — stock data + CrewAI chat side by side
- [x] Create `src/pages/Goals.jsx` — goal planning

## Phase 7: Integration & Testing
- [ ] Run dataset generation
- [ ] Run model training
- [ ] Start FastAPI backend
- [ ] Start React frontend
- [ ] Test JWT auth flow
- [ ] Test dashboard with/without transactions
- [ ] Test AI Assistant (finance-only, rejects non-finance)
- [ ] Test Stock Analysis (data + chat side by side)

## Phase 8: Documentation
- [ ] Create walkthrough
## Phase 8: Deployment & Tracking
- [x] Initial GitHub push (README.md, .gitignore)
