#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
python3 -B verify.py | diff -u EXPECTED_OUTPUT.txt -
python3 -B -m unittest -v
sha256sum -c SHA256SUMS
