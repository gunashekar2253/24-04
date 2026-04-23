@echo off
setlocal
color 0A

echo ===================================================
echo     FINANCE AI DASHBOARD - SYSTEM INITIALIZER
echo ===================================================
echo.

:: 1. Verify Python Installation
echo [*] Checking Python Installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in System PATH!
    echo Please install Python 3.10+ from python.org and try again.
    pause
    exit /b 1
)

:: 2. Verify Node.js Installation
echo [*] Checking Node.js Installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in System PATH!
    echo Please install Node.js from nodejs.org and try again.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo     STARTING BACKEND ORCHESTRATION (FASTAPI)
echo ===================================================
cd backend

:: 3. Setup Virtual Environment dynamically
if not exist "venv\" (
    echo [*] Generating fresh Python Virtual Environment (venv)...
    python -m venv venv
)

:: 4. Install backend dependencies natively
echo [*] Installing locked ecosystem dependencies from requirements.txt...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
pip install -r requirements.txt

:: 5. Mount Uvicorn Server in a separate window
echo [*] Booting AI REST Engine on Port 8011...
start "AI Backend Server" cmd /k "call venv\Scripts\activate.bat && python -m uvicorn app.main:app --port 8011 --reload"

echo.
echo ===================================================
echo     STARTING FRONTEND ORCHESTRATION (VITE/REACT)
echo ===================================================
cd ..\frontend

:: 6. Setup Frontend dependencies
echo [*] Scanning Node Modules...
if not exist "node_modules\" (
    echo [*] Pulling massive React dependency tree (npm install)...
    call npm install
)

:: 7. Boot Frontend
echo [*] Booting Vite Dashboard Interface...
start "React Frontend Interface" cmd /k "npm run dev"

echo.
echo ===================================================
echo     SYSTEM ONLINE - CHECK NEW TERMINAL WINDOWS
echo ===================================================
pause
