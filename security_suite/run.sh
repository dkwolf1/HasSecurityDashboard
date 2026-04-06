#!/bin/bash
set -e

echo "Starting Security Suite..."
echo "Working directory: $(pwd)"
echo "Python version: $(python3 --version)"

cd /app
echo "Changed to: $(pwd)"
echo "Files in app:"
ls -la

echo "Activating virtual environment..."
source /opt/venv/bin/activate

echo "Python path: $PYTHONPATH"
echo "Installed packages:"
pip list

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8080
