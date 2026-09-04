#!/bin/sh
set -eu
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
task_tmp=$(mktemp -d)
trap 'rm -rf "$task_tmp"' EXIT HUP INT TERM
sha256sum -c SHA256SUMS
python3 enumerate_multiplicities.py > "$task_tmp/result.json"
cmp result.json "$task_tmp/result.json"
python3 audit_rows.py > "$task_tmp/audit.txt"
python3 audit_local_pairs.py >> "$task_tmp/audit.txt"
cmp EXPECTED_OUTPUT.txt "$task_tmp/audit.txt"
cat "$task_tmp/audit.txt"
printf '%s\n' 'PASS: exact incidence audit matches the committed evidence'
