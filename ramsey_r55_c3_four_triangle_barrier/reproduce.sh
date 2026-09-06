#!/usr/bin/env bash
set -euo pipefail
src=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo 'usage: reproduce.sh NEW_OUTPUT_DIRECTORY [--audit-only]' >&2
  exit 2
fi
if [ "$#" -eq 2 ] && [ "$2" != '--audit-only' ]; then
  echo 'unknown option' >&2
  exit 2
fi
if [ -e "$1" ]; then
  echo 'output directory must not exist' >&2
  exit 2
fi
mkdir -p -- "$1"
out=$(CDPATH='' cd -- "$1" && pwd)
cd -- "$src"
sha256sum -c SHA256SUMS
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror block.cpp -o "$out/block"
run="$src"
if [ "$#" -eq 1 ]; then
  "$out/block" baseline.edges "$out/full" 0 1001 22 123
  cmp blocks.tsv "$out/full/blocks.tsv"
  cmp best.edges "$out/full/best.edges"
  run="$out/full"
else
  echo 'AUDIT ONLY: recorded production minima are not re-evaluated'
fi
python3 -B audit.py baseline.edges "$run" --count 1001 --bits 22 --output "$out/verification.json"
cmp verification.json "$out/verification.json"
python3 -B -O audit.py baseline.edges "$run" --count 1001 --bits 22 --output "$out/verification-optimized.json"
cmp verification.json "$out/verification-optimized.json"
"$out/block" baseline.edges "$out/small" 0 1 8 123 "$out/control-table.txt"
cmp control-table.txt "$out/control-table.txt"
python3 -B audit.py baseline.edges "$out/small" --count 1 --bits 8 --table "$out/control-table.txt" --controls --output "$out/small-audit.json"
cmp small-audit.json "$out/small-audit.json"
python3 -B count.py > "$out/count.json"
cmp count.json "$out/count.json"
python3 -B -O count.py > "$out/count-optimized.json"
cmp count.json "$out/count-optimized.json"
python3 -B - <<'PY'
import csv
rows = list(csv.DictReader(open('blocks.tsv'), delimiter='\t'))
if len(rows) != 1001 or any(int(r['minimum']) != 123 or int(r['first_mask']) != 0
                          or int(r['multiplicity']) != 1 for r in rows):
    raise ValueError('recorded unique-minimum claim')
print('All recorded minima: 123, unique at zero; distinct family size: 4183743579')
PY
