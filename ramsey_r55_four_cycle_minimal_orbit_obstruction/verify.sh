#!/usr/bin/env bash
set -euo pipefail

python3 verify_proofs.py
python3 -m unittest -v test_rup.py
