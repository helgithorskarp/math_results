#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
audit_output="$(python3 verify.py)"
optimized_output="$(python3 -O verify.py)"
test "$audit_output" = "$optimized_output"
printf '%s\n' "$audit_output"
python3 -m unittest -v test_verify.py
sha256sum --check SHA256SUMS
