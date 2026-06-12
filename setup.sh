#!/bin/bash

# NeoRunner Backend Setup Script

echo "🚀 Setting up NeoRunner Backend..."

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your PostgreSQL credentials"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your PostgreSQL connection details"
echo "2. Start PostgreSQL: docker-compose up -d"
echo "3. Run the server: python main.py"
echo "4. Visit: http://localhost:8000/docs for API documentation"
