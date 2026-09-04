#!/bin/sh
set -eu
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
task_tmp=$(mktemp -d)
trap 'rm -rf "$task_tmp"' EXIT HUP INT TERM
sha256sum -c SHA256SUMS
python3 generate_formula.py > "$task_tmp/model.cnf"
python3 verify.py --cnf "$task_tmp/model.cnf" > "$task_tmp/output.txt"
g++ -std=c++17 -O2 -Wall -Wextra -Werror enumerate.cpp -o "$task_tmp/enumerate"
"$task_tmp/enumerate" "$task_tmp/fixture18.edges" >> "$task_tmp/output.txt"
cmp fixture18.edges "$task_tmp/fixture18.edges"
cmp EXPECTED_OUTPUT.txt "$task_tmp/output.txt"
cat "$task_tmp/output.txt"
printf '%s\n' 'PASS: order-three type 1^22 3^7 is excluded'
