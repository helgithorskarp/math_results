#!/usr/bin/env bash
set -euo pipefail
core_switch_src=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
core_switch_run=${1:-$(mktemp -d /tmp/r55-core186-switch.XXXXXX)}
mkdir -p "$core_switch_run"
python3 -B "$core_switch_src/check_certificate.py" "$core_switch_src/obstruction.dimacs" "$core_switch_src/certificate.drat.txt" --output "$core_switch_run/certificate_verification.json"
python3 -B "$core_switch_src/controls.py" --output "$core_switch_run/controls.json"
python3 -B "$core_switch_src/certificate_controls.py" "$core_switch_src/obstruction.dimacs" "$core_switch_src/certificate.drat.txt" --output "$core_switch_run/certificate_controls.json"
for core_switch_file in certificate_verification.json controls.json certificate_controls.json; do
  cmp "$core_switch_run/$core_switch_file" "$core_switch_src/$core_switch_file"
done
if [[ "${2:-}" == "--full" ]]; then
  python3 -B "$core_switch_src/generate.py" --out "$core_switch_run/generated"
  python3 -B "$core_switch_src/verify_formula.py" --work "$core_switch_run/generated" --output "$core_switch_run/generated/verification.json"
  for core_switch_file in core.edges labels.json summary.json verification.json; do
    cmp "$core_switch_run/generated/$core_switch_file" "$core_switch_src/$core_switch_file"
  done
elif [[ -n "${2:-}" ]]; then
  printf 'Expected optional second argument --full\n' >&2
  exit 2
fi
printf 'Verified saved Core186 induced-core switching-class exclusion; state: %s\n' "$core_switch_run"
