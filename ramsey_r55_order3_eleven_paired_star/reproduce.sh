#!/usr/bin/env bash
set -euo pipefail
paired_star_src=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
paired_star_run=${1:-$(mktemp -d /tmp/r55-paired-star.XXXXXX)}
paired_star_flags=(-B)
if [[ "${2:-}" == "--optimized" ]]; then
  paired_star_flags+=(-O)
elif [[ -n "${2:-}" ]]; then
  printf 'Expected optional second argument --optimized\n' >&2
  exit 2
fi
mkdir -p "$paired_star_run"
python3 "${paired_star_flags[@]}" "$paired_star_src/produce.py" --out "$paired_star_run/generated"
python3 "${paired_star_flags[@]}" "$paired_star_src/verify.py" --work "$paired_star_run/generated" --report "$paired_star_run/verification.json"
python3 "${paired_star_flags[@]}" "$paired_star_src/controls.py" --report "$paired_star_run/controls.json"
for paired_star_file in coefficients.json result.json; do
  cmp "$paired_star_run/generated/$paired_star_file" "$paired_star_src/$paired_star_file"
done
cmp "$paired_star_run/generated/winner.edges" "$paired_star_src/input.edges"
cmp "$paired_star_run/verification.json" "$paired_star_src/verification.json"
cmp "$paired_star_run/controls.json" "$paired_star_src/controls.json"
printf 'Verified complete paired-star certificate; generated tables retained in %s\n' "$paired_star_run"
