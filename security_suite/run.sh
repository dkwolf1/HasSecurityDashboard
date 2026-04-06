#!/bin/bash
set -e

echo "Starting HasSecurityDash..."
echo "Working directory: $(pwd)"

cd /app
echo "Changed to: $(pwd)"
echo "Files in app:"
ls -la
echo "Files in app/app:"
ls -la app/app/

echo "Activating virtual environment..."
source /opt/venv/bin/activate

echo "Python version: $(python --version)"
echo "Installed packages:"
pip list

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8081
