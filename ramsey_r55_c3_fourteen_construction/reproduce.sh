#!/usr/bin/env bash
set -euo pipefail
src=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
if [ "$#" -ne 1 ]; then
  echo 'usage: reproduce.sh NEW_OUTPUT_DIRECTORY' >&2
  exit 2
fi
if [ -e "$1" ]; then
  echo 'output directory must not exist' >&2
  exit 2
fi
mkdir -p -- "$1"
out=$(CDPATH='' cd -- "$1" && pwd)
cd -- "$src"
sha256sum -c SHA256SUMS
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror induced.cpp -o "$out/induced"
python3 -B verify.py . --restarts 16 --steps 25000 --seed-base 202609061 --output "$out/verification.json"
cmp verification.json "$out/verification.json"
python3 -B -O verify.py . --restarts 16 --steps 25000 --seed-base 202609061 --output "$out/verification-optimized.json"
cmp verification.json "$out/verification-optimized.json"
python3 -B controls.py --output "$out/controls.json"
cmp controls.json "$out/controls.json"
python3 -B -O controls.py --output "$out/controls-optimized.json"
cmp controls.json "$out/controls-optimized.json"
python3 -B compare.py best.edges "$out/induced" "$out/comparison"
cmp comparison.json "$out/comparison/comparison.json"
cmp comparison_decisions.txt "$out/comparison/decisions.txt"
python3 -B -O compare.py best.edges "$out/induced" "$out/comparison-optimized"
cmp comparison.json "$out/comparison-optimized/comparison.json"
cmp comparison_decisions.txt "$out/comparison-optimized/decisions.txt"
python3 -B compare_controls.py "$out/induced" "$out/comparison-controls"
cmp comparison_controls.json "$out/comparison-controls/controls.json"
python3 -B -O compare_controls.py "$out/induced" "$out/comparison-controls-optimized"
cmp comparison_controls.json "$out/comparison-controls-optimized/controls.json"
echo 'VERIFIED score 123 (72 blue, 51 red); separation and controls pass'
