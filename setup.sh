#!/bin/bash

# Data Engineering Learning Agent Setup Script
# This script will set up your learning environment quickly

echo "🚀 Setting up your Data Engineering Learning Agent..."
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o 'Python [0-9]\.[0-9]' | grep -o '[0-9]\.[0-9]')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version detected (>= 3.8 required)"
else
    echo "❌ Python 3.8+ required. Current version: $python_version"
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv learning-agent-env
source learning-agent-env/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "⚙️ Creating environment configuration..."
    cp .env.template .env
    echo "📝 Please edit .env file and add your Claude API key"
else
    echo "✅ Environment file already exists"
fi

# Create data directory for progress tracking
mkdir -p data
echo "📁 Created data directory for progress tracking"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Claude API key:"
echo "   ANTHROPIC_API_KEY=your_key_here"
echo ""
echo "2. Activate the environment and run the agent:"
echo "   source learning-agent-env/bin/activate"
echo "   streamlit run data_engineering_agent.py"
echo ""
echo "3. Open your browser to the URL shown by Streamlit"
echo ""
echo "Happy learning! 🚀"
