**`PROJECT_SUMMARY.md`**
# AI Weatherman – Sunny McSkies – Project Summary (Dec 2025)

## Goal
Build a **100% free**, fully automated, personal daily weather forecast delivered every morning with a fun, light-hearted, TV-weatherman-style report powered by a massive open-source LLM.

## Core Features Achieved
- Fetches real-time daily + hourly weather data from **Open-Meteo** (no API key needed)
- Uses **Hugging Face Inference Router** + huge open models (e.g. `openai/gpt-oss-120b:groq` or Llama-3.1-405B) via OpenAI-compatible client – completely free with generous rate limits
- Generates a cheerful, personalized forecast written by “Sunny McSkies”
- Delivers the report instantly via **ntfy.sh** (free push notifications to phone/desktop)
- Entire pipeline runs automatically every morning at 6 AM local time via **cron**

## Tech Stack (all free / standard library)
- Python 3 + `urllib.request`, `json`, `textwrap`, `datetime`
- `openai` Python client (for HF router)
- `python-dotenv` for secrets
- Open-Meteo API (no key)
- Hugging Face Inference (free tier)
- ntfy.sh (free push notifications)
- Cron (system scheduler)

## Repository Structure

ai-weatherman-repo/
├── src/
│   ├── openmeteo.py       → fetches & saves daily/hourly JSON
│   ├── weatherman.py      → LLM prompt + report + ntfy delivery
│   └── run_weather.sh     → master bash script (runs both Python scripts)
├── data/
│   ├── daily_forecast.json, hourly_forecast.json, weather_report.txt
|   └── logs/
|       ├── openmeteo.log, weatherman.log
|       └── cron.log               → execution log
├── .env                   → HF_TOKEN (and optional others)


## Automation
Uses a Github Actions workflow to automate delivery of weather broadcast.

## Delivery Method: ntfy.sh
- Zero cost, zero accounts
- Users just install the ntfy app (iOS/Android) or visit https://ntfy.sh/sunny-roundrock
- Future-proof for consumer self-serve: anyone can subscribe to their own city topic (e.g. `sunny-austin`, `sunny-90210`) → perfect scaling path chosen

## Current Status
- Fully working end-to-end
- Runs daily at 7 AM Central Time
- Delivers forecast to phone via ntfy (subscribe to 'sunny-roundrock')
- Zero ongoing cost
- Ready for future expansion (multi-city, consumer location input, emojis, etc.)

Sunny McSkies is officially live and waking up Central Texas every morning. ☀️
