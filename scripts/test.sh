#!/usr/bin/env bash
# Single entry point for the test system. Run after every change.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m pytest -q tests "$@"
