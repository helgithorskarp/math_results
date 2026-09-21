#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
