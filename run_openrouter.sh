#!/bin/bash
# Quick start script for Panda Pick & Place with OpenRouter

set -e

echo "=========================================="
echo "Panda Pick & Place - Quick Start"
echo "=========================================="
echo ""

# Check if OPENROUTER_API_KEY is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "ERROR: OPENROUTER_API_KEY is not set!"
    echo ""
    echo "Please set your OpenRouter API key:"
    echo "  export OPENROUTER_API_KEY='your-key-here'"
    echo ""
    echo "Get your key from: https://openrouter.ai/"
    exit 1
fi

echo "✓ OPENROUTER_API_KEY is set"
echo ""

# Default model (Mistral Large is available in your region)
# Available models verified: mistralai/mistral-large, deepseek/deepseek-chat
MODEL="${LLM_MODEL:-google/gemini-3-flash-preview}"
echo "Using model: $MODEL"
echo ""
echo "Tip: Set LLM_MODEL to use a different model:"
echo "  export LLM_MODEL='deepseek/deepseek-chat'"
echo "  Run 'python diagnose_openrouter.py' to find more available models"
echo ""

# Default max steps
MAX_STEPS="${1:-50}"
echo "Running with max-steps: $MAX_STEPS"
echo ""

echo "=========================================="
echo "Starting LLM-powered Pick & Place..."
echo "=========================================="
echo ""

python main.py --mode llm --provider openrouter --max-steps "$MAX_STEPS"

echo ""
echo "=========================================="
echo "Demo completed!"
echo "=========================================="
