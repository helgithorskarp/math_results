#!/bin/sh
set -eu

if [ "$#" -ne 3 ]; then
    echo "usage: $0 SCRATCH_OUTPUT_DIR CADICAL DRAT_TRIM" >&2
    exit 2
fi

output=$1
cadical=$2
drat_trim=$3
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

mkdir -p "$output"
cnf="$output/degree_pattern_a4.cnf"
proof="$output/degree_pattern_a4.drat"
solver_log="$output/solver.log"
checker_log="$output/checker.log"

python3 "$script_dir/generate_cnf.py" "$cnf"
python3 "$script_dir/audit.py"
python3 "$script_dir/verify_witnesses.py"

status=0
"$cadical" "$cnf" "$proof" >"$solver_log" 2>&1 || status=$?
if [ "$status" -ne 20 ]; then
    echo "solver did not prove UNSAT (exit $status)" >&2
    exit 1
fi
"$drat_trim" "$cnf" "$proof" >"$checker_log" 2>&1
grep -q 's VERIFIED' "$checker_log"

sha256sum "$cnf" "$proof"
echo "degree pattern (5^4,4,3^7) is UNSAT and DRAT-verified"
