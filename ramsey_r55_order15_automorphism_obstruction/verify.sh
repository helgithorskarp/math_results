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
python3 verify_cycle_types.py --result "$task_tmp/cycle_types.json"

"$task_cxx" -O3 -std=c++20 -Wall -Wextra -Wpedantic \
  verify_formula.cpp -o "$task_tmp/verify_formula"

counts=("1 4 2 2" "2 1 0 8" "2 1 1 5" "2 1 2 2" "2 2 0 3" "2 2 1 0")
for index in 0 1 2 3 4 5; do
  formula="$task_tmp/formula_$index.cnf"
  python3 generate_formula.py --case "$index" "$formula"
  read -r cycles15 cycles5 cycles3 fixed <<< "${counts[$index]}"
  "$task_tmp/verify_formula" "$cycles15" "$cycles5" "$cycles3" "$fixed" "$formula"
  proof="proof_a${cycles15}_${cycles5}_${cycles3}_${fixed}.drat.xz"
  xz -t "$proof"
  xz -dc "$proof" | "$task_drat" "$formula" -I
done
