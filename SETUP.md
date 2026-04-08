# Finance AI - Local Setup Guide

Follow these steps to clone and run the Finance AI project on a new system. 

## Prerequisites
Ensure the following software is installed on your new system:
- **Git** (for version control)
- **Node.js & npm** (version 18+ recommended for the frontend)
- **Python** (version 3.10+ recommended for the backend)

## Step 1: Clone the Repository
Open your terminal or command prompt and run the following command to clone the code into your desired directory:
```bash
git clone <YOUR_GITHUB_REPO_URL>
cd project-at
```
*(Note: Replace `<YOUR_GITHUB_REPO_URL>` with the actual URL of your GitHub repository)*

## Step 2: Backend Setup 
The backend handles the AI models, SQLite database, and API endpoints via FastAPI.

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create calculating virtual environment (recommended to isolate dependencies):
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows:** 
     ```bash
     .\venv\Scripts\activate
     ```
   - **Mac/Linux:** 
     ```bash
     source venv/bin/activate
     ```
4. Install all required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up the Environment Variables by creating a `.env` file in the `backend` folder:
   ```bash
   SECRET_KEY=your_super_secret_jwt_key
   GEMINI_API_KEY=your_google_gemini_api_key
   ```
6. Seed the SQLite Database with initial mock data (optional but recommended for a quick start):
   ```bash
   python scripts/seed_db.py
   ```
7. Start the backend server:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   *The backend should now be running at http://localhost:8000.*

## Step 3: Frontend Setup
The frontend is a Vite + React application.

1. Open a **new, separate terminal window**.
2. Navigate to the frontend directory:
   ```bash
   cd project-at/frontend
   ```
3. Install all Node.js dependencies:
   ```bash
   npm install
   ```
4. Start the frontend development server:
   ```bash
   npm run dev
   ```
   *The frontend should now be running at http://localhost:5173.*

## Step 4: Access the Application
1. Open your web browser and go to `http://localhost:5173`.
2. Because you ran the `seed_db.py` script, you can log in using the default testing credentials:
   - **Username:** `testuser`
   - **Password:** `password123`

You should now have the identical "Finance AI" interface up and running flawlessly!
