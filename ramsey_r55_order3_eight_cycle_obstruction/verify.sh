#!/bin/sh
set -eu
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
PYTHONDONTWRITEBYTECODE=1 python3 reproduce.py "$@"
