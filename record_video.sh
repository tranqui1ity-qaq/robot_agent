#!/bin/bash
# Record Panda Pick & Place robot demo as MP4 video

set -e

echo "=========================================="
echo "Panda Pick & Place - Video Recording"
echo "=========================================="
echo ""

# Get parameters from command line or use defaults
OUTPUT="${1:-robot_demo.mp4}"
MAX_STEPS="${2:-50}"
FRAMES_PER_STEP="${3:-20}"
PROVIDER="${4:-openrouter}"
FPS="${5:-60}"

# Validate provider
if [[ "$PROVIDER" != "openrouter" && "$PROVIDER" != "openai" ]]; then
    echo "Error: PROVIDER must be 'openrouter' or 'openai', got: $PROVIDER"
    echo ""
    echo "Usage: bash record_video.sh [output.mp4] [max_steps] [frames_per_step] [provider] [fps]"
    echo ""
    echo "Examples:"
    echo "  bash record_video.sh                              # Uses defaults"
    echo "  bash record_video.sh demo.mp4 50 20 openrouter 60"
    echo "  bash record_video.sh demo.mp4 30 15 openai 60"
    exit 1
fi

# Check for required API key
if [ "$PROVIDER" = "openrouter" ]; then
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
    MODEL_VAR="OpenRouter"
    DEFAULT_MODEL="mistralai/mistral-large"
elif [ "$PROVIDER" = "openai" ]; then
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "ERROR: OPENAI_API_KEY is not set!"
        echo ""
        echo "Please set your OpenAI API key:"
        echo "  export OPENAI_API_KEY='your-key-here'"
        echo ""
        echo "Get your key from: https://platform.openai.com/account/api-keys"
        exit 1
    fi
    echo "✓ OPENAI_API_KEY is set"
    MODEL_VAR="OpenAI"
    DEFAULT_MODEL="gpt-4o-mini"
fi

echo ""
echo "Recording configuration:"
echo "  Provider: $PROVIDER ($MODEL_VAR)"
echo "  Output: videos/$OUTPUT"
echo "  Max steps: $MAX_STEPS"
echo "  Frames per step: $FRAMES_PER_STEP"
echo "  FPS: $FPS"
echo ""

# Get model from environment or use default
MODEL="${LLM_MODEL:-$DEFAULT_MODEL}"
echo "Using model: $MODEL"
echo "(Set LLM_MODEL to use different model)"
echo ""

echo "=========================================="
echo "Starting video recording..."
echo "=========================================="
echo ""

python record_video.py \
    --output "$OUTPUT" \
    --max-steps "$MAX_STEPS" \
    --frames-per-step "$FRAMES_PER_STEP" \
    --provider "$PROVIDER" \
    --fps "$FPS"

echo ""
echo "=========================================="
echo "Recording completed!"
echo "=========================================="
echo ""
echo "Video saved to: videos/$OUTPUT"
echo ""
echo "To play the video:"
echo "  ffplay videos/$OUTPUT"
echo "  vlc videos/$OUTPUT"
