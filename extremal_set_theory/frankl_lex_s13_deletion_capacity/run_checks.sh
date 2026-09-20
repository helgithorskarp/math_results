#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 verify.py
python3 independent_check.py
python3 -m unittest -v test_verify.py
