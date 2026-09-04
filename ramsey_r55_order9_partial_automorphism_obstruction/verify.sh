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

indices=(0 1 2 3 4 6 7)
counts=("3 0 16" "3 1 13" "3 2 10" "3 3 7" "3 4 4" "4 0 7" "4 1 4")
for position in 0 1 2 3 4 5 6; do
  index=${indices[$position]}
  read -r cycles9 cycles3 fixed <<< "${counts[$position]}"
  degree=0
  degree_option=()
  proof="proof_a${cycles9}_${cycles3}_${fixed}.drat.xz"
  if [[ $index == 7 ]]; then
    degree=1
    degree_option=(--degree)
    proof="proof_a${cycles9}_${cycles3}_${fixed}_degree.drat.xz"
  fi
  formula="$task_tmp/formula_$index.cnf"
  python3 generate_formula.py --case "$index" "${degree_option[@]}" "$formula"
  "$task_tmp/verify_formula" "$cycles9" "$cycles3" "$fixed" "$degree" "$formula"
  xz -t "$proof"
  xz -dc "$proof" | "$task_drat" "$formula" -I
done
