#!/usr/bin/env bash
# Launches the TPGP Generator locally and opens it in your browser.
set -e
cd "$(dirname "$0")"

if ! python3 -c "import flask" 2>/dev/null; then
  echo "Installing dependencies (first run only)..."
  pip3 install -r requirements.txt
fi

PORT="${TPGP_PORT:-8200}"
URL="http://127.0.0.1:${PORT}"
echo "Starting TPGP Generator at ${URL} ..."

( sleep 1.5
  if command -v open >/dev/null 2>&1; then open "$URL"
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL"
  fi
) &

python3 app.py
