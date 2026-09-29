#!/usr/bin/env bash
# Script wrapper de Rollback e Expurgo — Projeto Cenário de Objetivos (2026)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" &>/dev/null; then
    PYTHON_BIN="python"
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/rollback_honeypot.py" "$@"
