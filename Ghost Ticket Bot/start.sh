#!/bin/sh

# Start bot and web services
cd bot && python bot.py &
cd ../web && uvicorn main:app --host 0.0.0.0 --port 8000
chmod +x start.sh
