#!/bin/sh
set -eu
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
