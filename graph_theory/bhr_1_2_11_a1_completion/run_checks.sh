#!/bin/sh
set -eu

python3 verify.py certificate.json --grid 5
python3 independent_check.py certificate.json
python3 audit_coverage.py coverage_data.json certificate.json
python3 -m unittest -v test_verify.py
