#!/usr/bin/env bash
set -euo pipefail

task_dir=$(cd "$(dirname "$0")" && pwd)
task_tmp=$(mktemp -d)
trap 'rm -rf -- "$task_tmp"' EXIT
task_drat=${DRAT_TRIM:-drat-trim}
task_cxx=${CXX:-g++}

cd "$task_dir"
python3 build_manifest.py --result "$task_tmp/result.json"
cmp result.json "$task_tmp/result.json"
python3 -m unittest -v test_exact.py

"$task_cxx" -O3 -std=c++20 -Wall -Wextra -Wpedantic \
  verify_formula.cpp -o "$task_tmp/verify_formula"

for fixed in 13 18 23 28; do
  formula="$task_tmp/p5f${fixed}.cnf"
  proof="proofs/p5f${fixed}.drat.xz"
  python3 generate_formula.py --prime 5 --fixed "$fixed" "$formula"
  "$task_tmp/verify_formula" "$fixed" "$formula"
  xz -t "$proof"
  xz -dc "$proof" | "$task_drat" "$formula" -I
done
