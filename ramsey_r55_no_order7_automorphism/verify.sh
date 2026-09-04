#!/usr/bin/env bash
set -euo pipefail

task_dir=$(cd "$(dirname "$0")" && pwd)
task_tmp=$(mktemp -d)
trap 'rm -rf -- "$task_tmp"' EXIT
task_drat=${DRAT_TRIM:-drat-trim}
task_cxx=${CXX:-g++}

declare -A formula_hash=(
  [15]=c55f4f7b526389c66b9d6c22643c386b1116737f30878fdbea4e15354d4686d6
  [22]=3f99803c30ba974f0f77cfe0773c70c94917b7da48ac10c0520c9e89f6c3379f
  [29]=3fa71beafaee42e3e80ae59f376a15fb88e77bff5cb06e3443004a0d4b44d411
  [36]=75910f34d8b242fa17348a38d295ff3144584dd9a3b5f655963a531410d6ac51
)

cd "$task_dir"
sha256sum -c SHA256SUMS
python3 -m unittest -v test_exact.py
"$task_cxx" -O3 -std=c++20 -Wall -Wextra -Wpedantic \
  verify_formula.cpp -o "$task_tmp/verify_formula"

for fixed in 15 22 29 36; do
  formula="$task_tmp/f${fixed}.cnf"
  proof="proof-f${fixed}.drat.xz"
  python3 generate_formula.py --fixed "$fixed" "$formula"
  printf '%s  %s\n' "${formula_hash[$fixed]}" "$formula" | sha256sum -c -
  "$task_tmp/verify_formula" "$fixed" "$formula"
  xz -t "$proof"
  xz -dc "$proof" | "$task_drat" "$formula" -i
done
