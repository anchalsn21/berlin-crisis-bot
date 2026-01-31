#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

if [ -d "venv" ]; then
    source venv/bin/activate
fi

PORT=${PORT:-7860}
MODEL_PATH="models/crisis-bot.tar.gz"

echo "Starting Rasa server on port $PORT..."

if [ -f "$MODEL_PATH" ]; then
    echo "Using model: $MODEL_PATH"
    python -m rasa run --enable-api --cors '*' --port "$PORT" --model "$MODEL_PATH"
else
    echo "Warning: Model not found. Training will be required."
    python -m rasa run --enable-api --cors '*' --port "$PORT"
fi
