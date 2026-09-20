#!/bin/sh
set -eu
sha256sum -c SHA256SUMS
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
