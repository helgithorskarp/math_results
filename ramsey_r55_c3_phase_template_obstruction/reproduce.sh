#!/usr/bin/env bash
set -euo pipefail
src=$(cd -- "$(dirname -- "$0")" && pwd)
if [[ $# -lt 1 || $# -gt 2 ]]; then echo 'usage: reproduce.sh FRESH_OUTPUT [--search]' >&2; exit 2; fi
out=$1
if [[ $# == 2 && $2 != --search ]]; then echo 'unknown option' >&2; exit 2; fi
if [[ -e "$out" ]]; then echo 'fresh output required' >&2; exit 2; fi
mkdir -p -- "$out"
out=$(cd -- "$out" && pwd)
(cd "$src" && sha256sum -c SHA256SUMS)
python3 -B "$src/proof.py" "$src/baseline.edges" "$src/traded.edges" > "$out/proof.json"
cmp "$out/proof.json" "$src/proof.json"
mkdir "$out/template"
cp -- "$src/template.py" "$src/physical.py" "$src/baseline.edges" "$out/template/"
python3 -B "$out/template/template.py" > "$out/template-run.json"
cmp "$out/template/template.json" "$src/template.json"
cmp "$out/template/traded.edges" "$src/traded.edges"
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror "$src/control.cpp" -o "$out/control"
"$out/control" "$src/traded.edges" > "$out/control.tsv"
cmp "$out/control.tsv" "$src/control.tsv"
python3 -B "$src/audit.py" "$src/traded.edges" "$out/control.tsv" --controls > "$out/controls.json"
cmp "$out/controls.json" "$src/controls.json"
python3 -B "$src/audit.py" "$src/traded.edges" "$src" > "$out/verification.json"
cmp "$out/verification.json" "$src/verification.json"
if [[ $# == 2 ]]; then
  g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror "$src/search.cpp" -o "$out/search"
  "$out/search" "$src/traded.edges" "$out/run" 16 25000 2026090621 5000
  for name in model.json restarts.tsv best.edges; do cmp "$out/run/$name" "$src/$name"; done
  python3 -B "$src/audit.py" "$src/traded.edges" "$out/run" > "$out/replay-audit.json"
  cmp "$out/replay-audit.json" "$src/verification.json"
fi
printf '%s\n' 'VERIFIED_FIXED_PHASE_OBSTRUCTION_AND_DEGREE_TRADE' 'VERIFIED_443_PHYSICAL_PHASE_CONTROLS' 'VERIFIED_PHASE_TRADE_GRAPH_SCORES: 177 defects; no target or traded-family exclusion'
