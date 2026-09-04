#!/usr/bin/env bash
set -euo pipefail

task_dir=$(cd "$(dirname "$0")" && pwd)
task_tmp=$(mktemp -d)
trap 'rm -rf -- "$task_tmp"' EXIT
task_drat=${DRAT_TRIM:-drat-trim}
task_cxx=${CXX:-g++}

cd "$task_dir"
sha256sum -c SHA256SUMS
python3 generate_formula.py "$task_tmp/formula.cnf"
printf '%s  %s\n' \
  'fdbd24c09d0163d1f524cbd0d35a6e55ee2308cc43409a419aa336b3dbab645a' \
  "$task_tmp/formula.cnf" | sha256sum -c -

"$task_cxx" -O3 -std=c++20 -Wall -Wextra -Wpedantic \
  verify_formula.cpp -o "$task_tmp/verify_formula"
"$task_tmp/verify_formula" "$task_tmp/formula.cnf"

xz -t proof.drat.xz
xz -dc proof.drat.xz | "$task_drat" "$task_tmp/formula.cnf" -i
