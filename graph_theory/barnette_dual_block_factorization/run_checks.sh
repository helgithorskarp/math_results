#!/bin/sh
set -eu
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u expected.json -
sha256sum -c SHA256SUMS
