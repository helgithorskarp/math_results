#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 verify.py --check-expected
python3 independent_check.py
python3 -m unittest -v test_classify.py
python3 ../odd_cycle_stacking_universal_certificate/universal_verify.py
sha256sum -c SHA256SUMS
