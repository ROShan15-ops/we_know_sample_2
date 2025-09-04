#!/bin/bash

echo "🚀 Setting up We Know - Recipe Ingredient Generator"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+ first."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Backend setup
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp env.example .env
    echo "⚠️  Please edit backend/.env and add your Spoonacular API key"
    echo "   Get your API key from: https://spoonacular.com/food-api"
else
    echo "✅ .env file already exists"
fi

cd ..

# Frontend setup
echo ""
echo "🎨 Setting up Frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Get your Spoonacular API key from: https://spoonacular.com/food-api"
echo "2. Edit backend/.env and add your API key"
echo "3. Start the backend: cd backend && source venv/bin/activate && python app.py"
echo "4. Start the frontend: cd frontend && npm start"
echo ""
echo "🌐 Backend will run on: http://localhost:5000"
echo "🎨 Frontend will run on: http://localhost:3000"
echo ""
echo "Happy cooking! 🍽️" 