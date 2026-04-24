# Finance AI System
A fully autonomous, multi-engine financial intelligence pipeline embedding XGBoost anomaly predictors, Prophet time-series models, CrewAI Wall Street agents, and an interactive Vite React dashboard.

## 🚀 1. Clone & Configuration
When you first clone this repository, you must generate a `.env` file to mount the LLMs:
```bash
git clone <your-repository-url>
cd project-at
```
Navigate into the `backend/` directory, create a file simply named `.env`, and insert your API keys:
```env
GEMINI_API_KEY="your-google-gemini-key-here"
OPENAI_API_KEY="your-openai-key-here" (optional, required if overriding Gemini in CrewAI bounds)
```


## 🤖 2. Data Synthesis & Model Compilation
Because Github strips out heavy Dataframes and `.pkl` generated files, you must mathematically generate the Machine Learning ecosystem from scratch on your local PC:

**Step A: Boot the Python Environment**
```bash
# From the backend directory
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Step B: Synthesize the Financial Dataset**
Generate 100,000+ rows of simulated financial banking geometry into `/data/processed/`.
```bash
python app/engine/generate_dataset.py
```

**Step C: Compile the Machine Learning Core**
You must chronologically train the AI engines across the generated data structure so the system learns the risk and velocity behaviors! Run the following compiler scripts:
```bash
# 1. Train the XGBoost Default Risk Predictor
python ml_models/train_risk_model.py

# 2. Train the Isolation Forest Behavior Anomaly Detector
python ml_models/train_anomaly_model.py

# 3. Train the Prophet Time-Series Forecaster
python ml_models/train_spending_model.py
```

## ⚡ 3. Launching the Ecosystem
Once the LLM datasets are compiled into `/ml_models/`, you can auto-launch the entire architectural stack utilizing the root layout deploy script:

Go back to the root (`c:\project-at\`) and double-click:
**`launch_system.bat`**

This will autonomously download all React Node dependencies, start the Uvicorn REST array (port 8011), and boot the dashboard interface seamlessly!
