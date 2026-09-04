#!/usr/bin/env bash
set -euo pipefail

compiler=${CXX:-g++}
"$compiler" -std=c++20 -O3 -Wall -Wextra -Wpedantic \
  enumerate_three_cycles.cpp -o enumerate_three_cycles
./enumerate_three_cycles > classification.regenerated.txt
cmp classification.txt classification.regenerated.txt
python3 verify_proofs.py
python3 verify_high_proofs.py
python3 -m unittest -v test_rup.py
