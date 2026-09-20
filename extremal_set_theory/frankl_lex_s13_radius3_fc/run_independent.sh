#!/bin/sh
set -eu
sha256sum -c SHA256SUMS
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
