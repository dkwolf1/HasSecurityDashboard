#!/bin/bash
set -e

echo "Starting HasSecurityDash..."
echo "Working directory: $(pwd)"
echo "Python version: $(python3 --version)"

cd /app
echo "Changed to: $(pwd)"
echo "Files in app:"
ls -la

echo "Starting FastAPI server..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080
