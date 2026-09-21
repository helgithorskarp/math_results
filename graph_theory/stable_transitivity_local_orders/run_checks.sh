#!/bin/sh
set -eu

export PYTHONDONTWRITEBYTECODE=1
python3 -m unittest -v test_verify.py
python3 verify.py
sha256sum -c SHA256SUMS
