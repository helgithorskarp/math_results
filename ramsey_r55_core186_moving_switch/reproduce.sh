#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 || $# -gt 2 || (${2:-} != '' && ${2:-} != '--full') ]]; then
    echo "Usage: bash reproduce.sh FRESH_OUTPUT_DIRECTORY [--full]" >&2
    exit 2
fi
source_dir=$(cd -- "$(dirname -- "$0")" && pwd)
mkdir -- "$1"
result_dir=$(cd -- "$1" && pwd)
python3 -B "$source_dir/check_rup.py" "$source_dir/obstruction.dimacs" "$source_dir/certificate.rup" --output "$result_dir/rup_verification.json"
python3 -B "$source_dir/rup_controls.py" "$source_dir/obstruction.dimacs" "$source_dir/certificate.rup" --output "$result_dir/rup_controls.json"
python3 -B "$source_dir/scope_controls.py" --output "$result_dir/scope_controls.json"
for name in rup_verification rup_controls scope_controls; do
    cmp "$result_dir/$name.json" "$source_dir/$name.json"
done
if [[ ${2:-} == '--full' ]]; then
    python3 -B "$source_dir/generate.py" --out "$result_dir/generated"
    python3 -B "$source_dir/verify_formula.py" --work "$result_dir/generated" --output "$result_dir/generated/verification.json"
    python3 -B "$source_dir/check_certificate.py" "$source_dir/obstruction.dimacs" "$source_dir/certificate.drat.txt" --output "$result_dir/certificate_verification.json"
    python3 -B "$source_dir/controls.py" --output "$result_dir/controls.json"
    python3 -B "$source_dir/certificate_controls.py" "$source_dir/obstruction.dimacs" "$source_dir/certificate.drat.txt" --output "$result_dir/certificate_controls.json"
    for name in core.edges labels.json summary.json verification.json; do
        cmp "$result_dir/generated/$name" "$source_dir/$name"
    done
    for name in certificate_verification controls certificate_controls; do
        cmp "$result_dir/$name.json" "$source_dir/$name.json"
    done
fi
echo 'PASS: moving33 switching-class exclusion and exact family scope'
