#!/usr/bin/env bash
set -euo pipefail

work_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_file=$(mktemp /tmp/complement-matching-total.XXXXXX)
trap 'rm -f "$output_file"' EXIT

cd "$work_dir"
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > "$output_file"
diff -u EXPECTED_OUTPUT.json "$output_file"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
