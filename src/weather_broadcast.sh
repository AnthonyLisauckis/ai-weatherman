#!/usr/bin/env bash
# Activate virtual env relative to this script's location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/.venv/bin/activate"
# weather_broadcast.sh - fetches updated weather + generates Sunny McSkies report to send via ntfy

# Exit on any error
set -e

# Go to the project directory
cd "$(dirname "$0")"/..

# Log start time
echo "["$(date)"] Starting weather broadcast..." >> $SCRIPT_DIR/data/logs/cron.log

# Step 1 - Fetch fresh Open-Meteo forecasts
echo "Fetching latest weather data..."
python3 src/openmeteo.py >> $SCRIPT_DIR/data/logs/openmeteo.log

# Step 2 - Generate report
echo "Generating report..."
python3 src/weatherman.py >> $SCRIPT_DIR/data/logs/weatherman.log

# Done!
echo "[$(date)] Sunny McSkies delivered successfully!" >> $SCRIPT_DIR/data/logs/cron.log
echo "Check your phone — Sunny just texted you"