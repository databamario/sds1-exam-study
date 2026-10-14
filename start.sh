#!/usr/bin/env bash
# One-click launcher for the SDS1 exam study app.
set -e
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "No virtual environment found. Setting it up now..."
  python3 -m venv .venv
  . .venv/bin/activate
  pip install -r requirements.txt
else
  . .venv/bin/activate
fi

echo
echo "Starting the app at http://localhost:8501"
echo "Press Ctrl+C to stop."
echo
exec streamlit run app.py
