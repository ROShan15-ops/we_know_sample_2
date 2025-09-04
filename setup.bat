@echo off
echo 🚀 Setting up We Know - Recipe Ingredient Generator
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 14+ first.
    pause
    exit /b 1
)

echo ✅ Python and Node.js are installed

REM Backend setup
echo.
echo 🔧 Setting up Backend...
cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy env.example .env
    echo ⚠️  Please edit backend\.env and add your Spoonacular API key
    echo    Get your API key from: https://spoonacular.com/food-api
) else (
    echo ✅ .env file already exists
)

cd ..

REM Frontend setup
echo.
echo 🎨 Setting up Frontend...
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
npm install

cd ..

echo.
echo ✅ Setup complete!
echo.
echo 📋 Next steps:
echo 1. Get your Spoonacular API key from: https://spoonacular.com/food-api
echo 2. Edit backend\.env and add your API key
echo 3. Start the backend: cd backend ^&^& venv\Scripts\activate ^&^& python app.py
echo 4. Start the frontend: cd frontend ^&^& npm start
echo.
echo 🌐 Backend will run on: http://localhost:5000
echo 🎨 Frontend will run on: http://localhost:3000
echo.
echo Happy cooking! 🍽️
pause 