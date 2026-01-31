#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "Starting Rasa actions server on port 5055..."
python -m rasa run actions --port 5055
