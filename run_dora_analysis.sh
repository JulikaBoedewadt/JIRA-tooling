#!/bin/bash

# DORA Metrics Analyzer Runner
# This script runs the DORA analysis from the main directory

echo "🚀 Running DORA Metrics Analysis..."
echo "=================================="

# Check if no arguments provided
if [ $# -eq 0 ]; then
    echo "❌ Error: Project name and key are required!"
    echo ""
    echo "Usage:"
    echo "  ./run_dora_analysis.sh --project-name \"Your Project\" --project-key \"YOUR\""
    echo ""
    echo "Any valid JIRA project key is supported"
    echo ""
    echo "Examples:"
    echo "  ./run_dora_analysis.sh --project-name \"Terminvereinbarung\" --project-key \"TEV\""
    echo "  ./run_dora_analysis.sh --project-name \"My Project\" --project-key \"MP\""
    echo "  ./run_dora_analysis.sh --project-name \"Web Analytics\" --project-key \"WA\""
    echo ""
    echo "For more options: ./run_dora_analysis.sh --help"
    exit 1
fi

# Change to DORA directory and run the analysis
cd DORA

# Check if virtual environment exists
if [ ! -d "dora_env" ]; then
    echo "📦 Setting up virtual environment..."
    python3 -m venv dora_env
    source dora_env/bin/activate
    pip install -r requirements.txt
else
    source dora_env/bin/activate
fi

# Run the analysis with all passed arguments
python3 dora_metrics_integrated.py "$@"

# Return to main directory
cd ..
