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
python3 verify_group_action.py --result "$task_tmp/action.json"
python3 generate_formula.py "$task_tmp/formula.cnf"

"$task_cxx" -O3 -std=c++20 -Wall -Wextra -Wpedantic \
  verify_formula.cpp -o "$task_tmp/verify_formula"
"$task_tmp/verify_formula" "$task_tmp/formula.cnf"

xz -t proof.drat.xz
xz -dc proof.drat.xz | "$task_drat" "$task_tmp/formula.cnf" -I -U
