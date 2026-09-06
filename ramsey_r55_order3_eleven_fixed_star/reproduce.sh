#!/usr/bin/env bash
set -euo pipefail
fixed_star_src=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
fixed_star_run=${1:-$(mktemp -d /tmp/r55-fixed-star.XXXXXX)}
mkdir -p "$fixed_star_run"
python3 -B "$fixed_star_src/produce.py" --out "$fixed_star_run/generated"
python3 -B "$fixed_star_src/verify.py" --work "$fixed_star_run/generated" --report "$fixed_star_run/verification.json"
python3 -B "$fixed_star_src/controls.py" --report "$fixed_star_run/controls.json"
cmp "$fixed_star_run/generated/certificate.json" "$fixed_star_src/certificate.json"
cmp "$fixed_star_run/generated/winner.edges" "$fixed_star_src/input.edges"
cmp "$fixed_star_run/verification.json" "$fixed_star_src/verification.json"
cmp "$fixed_star_run/controls.json" "$fixed_star_src/controls.json"
printf 'Verified exact fixed-star certificate; generated tables retained in %s\n' "$fixed_star_run"
