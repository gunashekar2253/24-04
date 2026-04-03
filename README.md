# AI Financial Decision System

A full-stack AI system for financial decision-making, risk prediction, and anomaly detection.

## Project Structure
- `backend/`: FastAPI backend with AI/ML engine.
- `frontend/`: React + Vite frontend.

## Features
- **Risk Prediction**: TensorFlow ReLU-based model.
- **Anomaly Detection**: Isolation Forest & Autoencoders.
- **Spending Forecast**: XGBoost & Prophet.
- **AI Assistant**: Finance-only Gemini API integration.
- **Stock Agent**: CrewAI + yFinance.

## Setup
1. Backend: 
   - `cd backend`
   - Create venv and `pip install -r requirements.txt`
   - `python -m app.main`
2. Frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`
