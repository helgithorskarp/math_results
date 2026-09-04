#!/usr/bin/env bash
set -euo pipefail

python3 verify_proofs.py
python3 verify_next_proofs.py
python3 verify_mid_proofs.py
python3 verify_high_proofs.py --only-cycle-type 1+6+18+18
python3 verify_high_proofs.py --exclude-cycle-type 1+6+18+18
python3 -m unittest -v test_rup.py
