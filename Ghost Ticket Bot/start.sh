#!/bin/sh

# Activate virtual environment (optional)
. /opt/venv/bin/activate

# Start bot
cd bot && python bot.py &

# Start web server (if using FastAPI/Flask)
cd ../web && uvicorn main:app --host 0.0.0.0 --port 8000

chmod +x start.sh
