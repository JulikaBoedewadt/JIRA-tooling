#!/bin/bash
# Unified DORA Metrics Analyzer - Simple Wrapper

echo "🚀 DORA Metrics Analyzer"
echo "========================"

# Check if we're in the right directory
if [ ! -f "analyze_dora.py" ]; then
    echo "❌ Error: Please run this script from the DORA directory"
    echo "   cd DORA && ./analyze.sh"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "dora_env" ]; then
    echo "📦 Setting up virtual environment..."
    python3 -m venv dora_env
    source dora_env/bin/activate
    pip install python-dateutil
    echo "✅ Setup completed!"
else
    echo "🔧 Activating virtual environment..."
    source dora_env/bin/activate
fi

# Run the unified analyzer
echo "🚀 Starting DORA analysis..."
python3 analyze_dora.py "$@"
