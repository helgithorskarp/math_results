#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$HERE"

PYTHONDONTWRITEBYTECODE=1 python3 verify.py certificate.json --grid 5
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py certificate.json
PYTHONDONTWRITEBYTECODE=1 python3 audit_coverage.py ../bhr_1_2_11_a1_completion/coverage_data.json certificate.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
