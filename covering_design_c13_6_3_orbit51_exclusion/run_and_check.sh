#!/bin/sh
set -eu

if [ "$#" -ne 3 ]; then
    echo "usage: $0 OUTPUT_DIR CADICAL DRAT_TRIM" >&2
    exit 2
fi

output=$1
cadical=$2
drat_trim=$3
jobs=${JOBS:-1}
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

mkdir -p "$output"
tasks="$output/tasks.txt"
: > "$tasks"

for case_name in c0_21 c1_12 c1_20 c2_03 c2_11 c3_02 c3_10
do
    for qpattern in 111 211
    do
        name=${case_name}_${qpattern}
        python3 "$script_dir/generate_dual_cnf.py" \
            "$output/$name.cnf" "$output/$name.json" \
            --case "$case_name" --qpattern "$qpattern"
        echo "$name" >> "$tasks"
    done
    for spec in \
        221:0000:0 221:0000:1 221:0010:0 221:0100:0 \
        222:0000:0 222:0000:1 222:0000:2 222:0010:0 \
        222:0010:1 222:0020:0 222:0110:0
    do
        old_ifs=$IFS
        IFS=:
        set -- $spec
        IFS=$old_ifs
        qpattern=$1
        qthrough=$2
        qaway=$3
        name=${case_name}_${qpattern}_${qthrough}_${qaway}
        python3 "$script_dir/generate_dual_cnf.py" \
            "$output/$name.cnf" "$output/$name.json" \
            --case "$case_name" --qpattern "$qpattern" \
            --qthrough "$qthrough" --qaway "$qaway"
        echo "$name" >> "$tasks"
    done
done

xargs -P "$jobs" -I '{}' sh -c '
    name=$1
    output=$2
    cadical=$3
    "$cadical" --unsat "$output/$name.cnf" "$output/$name.drat" \
        > "$output/$name.solver.log" 2>&1
    status=$?
    printf "%s %s\n" "$name" "$status" > "$output/$name.status"
    test "$status" -eq 20
' _ '{}' "$output" "$cadical" < "$tasks"

xargs -P "$jobs" -I '{}' sh -c '
    name=$1
    output=$2
    checker=$3
    "$checker" "$output/$name.cnf" "$output/$name.drat" \
        > "$output/$name.check.log" 2>&1
    grep -q "s VERIFIED" "$output/$name.check.log"
    printf "%s VERIFIED\n" "$name" > "$output/$name.check.status"
' _ '{}' "$output" "$drat_trim" < "$tasks"

PYTHONDONTWRITEBYTECODE=1 python3 "$script_dir/collect_results.py" \
    "$output/OBSERVED.json" "$output"
cmp "$script_dir/EXPECTED.json" "$output/OBSERVED.json"

PYTHONDONTWRITEBYTECODE=1 python3 "$script_dir/audit_encoding.py" \
    --expected "$script_dir/EXPECTED.json" > "$output/OBSERVED_AUDIT.json"
cmp "$script_dir/EXPECTED_AUDIT.json" "$output/OBSERVED_AUDIT.json"

echo "all 91 orbit-51 cases are UNSAT and DRAT-verified"
