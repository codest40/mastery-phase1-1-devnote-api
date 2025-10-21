#!/usr/bin/env bash
set -e

echo "Starting DevNotes FastAPI backend in production mode..."
exec gunicorn main:app \
  -k uvicorn.workers.UvicornWorker \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 4 \
  --timeout 60
