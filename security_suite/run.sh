#!/usr/bin/with-contenv bashio
set -e

cd /app
uvicorn app.main:app --host 0.0.0.0 --port 8080
