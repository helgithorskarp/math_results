#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

export PYTHONDONTWRITEBYTECODE=1
python3 verify.py | diff -u EXPECTED_OUTPUT.json -
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
