#!/usr/bin/env bash
set -euo pipefail

python3 verify.py
python3 -m unittest -v test_exact.py
