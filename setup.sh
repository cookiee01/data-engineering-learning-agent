#!/bin/bash

# Data Engineering Learning Agent Setup Script
# This script will set up your learning environment quickly

echo "🚀 Setting up your Data Engineering Learning Agent..."
echo ""

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 command not found"
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Get Python version more reliably
python_version=$(python3 --version 2>&1)
echo "🐍 Detected: $python_version"

# Extract version number more robustly
version_number=$(echo "$python_version" | sed 's/Python //' | cut -d. -f1,2)
major_version=$(echo "$version_number" | cut -d. -f1)
minor_version=$(echo "$version_number" | cut -d. -f2)

echo "📊 Parsed version: $major_version.$minor_version"

# Check if version is 3.8 or higher
if [ "$major_version" -eq 3 ] && [ "$minor_version" -ge 8 ]; then
    echo "✅ Python $version_number is compatible (>= 3.8 required)"
elif [ "$major_version" -gt 3 ]; then
    echo "✅ Python $version_number is compatible (>= 3.8 required)"
else
    echo "❌ Python 3.8+ required. Current version: $version_number"
    echo "Please install Python 3.8+ and try again."
    echo ""
    echo "💡 Tips for installing Python 3.8+:"
    echo "• macOS: brew install python@3.11"
    echo "• Ubuntu: sudo apt update && sudo apt install python3.11"
    echo "• Or visit: https://www.python.org/downloads/"
    exit 1
fi

# Check if we're already in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "📦 Virtual environment already active: $VIRTUAL_ENV"
    use_existing_venv=true
else
    use_existing_venv=false
fi

# Create virtual environment if not already in one
if [ "$use_existing_venv" = false ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv learning-agent-env
    
    echo "🔄 Activating virtual environment..."
    source learning-agent-env/bin/activate
    
    # Verify activation worked
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        echo "❌ Failed to activate virtual environment"
        echo "Please try manual setup:"
        echo "  python3 -m venv learning-agent-env"
        echo "  source learning-agent-env/bin/activate"
        echo "  pip install -r requirements.txt"
        exit 1
    fi
    
    echo "✅ Virtual environment activated: $VIRTUAL_ENV"
fi

# Upgrade pip to avoid installation issues
echo ""
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

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
echo "1. Get your Claude API key from: https://console.anthropic.com/"
echo "2. Edit .env file and add your API key:"
echo "   ANTHROPIC_API_KEY=your_key_here"
echo ""
if [ "$use_existing_venv" = false ]; then
    echo "3. Activate the environment and run the agent:"
    echo "   source learning-agent-env/bin/activate"
else
    echo "3. Run the agent (virtual environment already active):"
fi
echo "   streamlit run data_engineering_agent.py"
echo ""
echo "4. Open your browser to the URL shown by Streamlit"
echo ""
echo "🎯 Ready to start your AI-powered learning journey!"
echo ""
echo "💡 Need help? Check QUICK_START.md for detailed instructions"
