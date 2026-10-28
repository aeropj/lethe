#!/usr/bin/env bash
# One command: set up a local Python environment, install, and start the demo on http://localhost:8787.
# First start downloads the on-device model (~1.2 GB) and the GeoNames city list once; later starts are offline.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
if [ ! -d .venv ]; then
  if command -v uv >/dev/null 2>&1; then uv venv -q -p 3.12 .venv; else "$PY" -m venv .venv; fi
fi
# shellcheck disable=SC1091
source .venv/bin/activate
if [ ! -f .venv/.installed ]; then
  echo "Installing (first run only)…"
  if command -v uv >/dev/null 2>&1; then INSTALL="uv pip install -q"; else python -m pip install -q --upgrade pip; INSTALL="python -m pip install -q"; fi
  if [ "$(uname)" = "Linux" ]; then $INSTALL --index-url https://download.pytorch.org/whl/cpu "torch>=2.5"; fi   # CPU-only build
  $INSTALL -r requirements.txt
  touch .venv/.installed
fi
exec python server.py
