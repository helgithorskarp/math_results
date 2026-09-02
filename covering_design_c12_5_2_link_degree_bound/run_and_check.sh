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

mkdir -p "$output/cnf" "$output/proofs" "$output/logs"
python3 "$script_dir/generate_instances.py" "$output/cnf"
python3 "$script_dir/audit.py"

for cnf in "$output"/cnf/*.cnf; do
    name=$(basename "$cnf" .cnf)
    proof="$output/proofs/$name.drat"
    solver_log="$output/logs/$name.solver.log"
    checker_log="$output/logs/$name.checker.log"
    status=0
    "$cadical" "$cnf" "$proof" >"$solver_log" 2>&1 || status=$?
    if [ "$status" -ne 20 ]; then
        echo "solver did not prove UNSAT for $name (exit $status)" >&2
        exit 1
    fi
    "$drat_trim" "$cnf" "$proof" >"$checker_log" 2>&1
    grep -q 's VERIFIED' "$checker_log"
done

sha256sum "$output"/cnf/*.cnf > "$output/cnf.sha256"
(
    cd "$output/proofs"
    sha256sum ./*.drat | sed 's#  \./#  #'
) > "$output/proofs.sha256"
if cmp -s "$output/proofs.sha256" "$script_dir/proof_hashes.sha256"; then
    echo "proof hashes match the pinned production run"
else
    echo "proofs verified; hashes differ from the pinned solver build"
fi
echo "all 35 instances UNSAT and DRAT-verified"
