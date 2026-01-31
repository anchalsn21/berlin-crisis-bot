#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "Training Rasa model..."
python -m rasa train --fixed-model-name crisis-bot

if [ $? -eq 0 ]; then
    echo "Model training completed successfully."
    echo "Model saved at: models/crisis-bot.tar.gz"
else
    echo "Model training failed."
    exit 1
fi
