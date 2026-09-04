#!/bin/sh
set -eu

task_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
task_tmp=$(mktemp -d)
trap 'rm -rf -- "$task_tmp"' EXIT HUP INT TERM
task_drat_trim=${DRAT_TRIM:-drat-trim}

python3 "$task_dir/verify.py" --rat-cnf "$task_tmp/p13f17.cnf"
xz -dc "$task_dir/proofs/p13f17.drat.xz" > "$task_tmp/p13f17.drat"
"$task_drat_trim" "$task_tmp/p13f17.cnf" "$task_tmp/p13f17.drat"
python3 -m unittest -v "$task_dir/test_exact.py"
