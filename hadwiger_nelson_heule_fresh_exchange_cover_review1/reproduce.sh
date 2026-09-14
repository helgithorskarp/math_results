#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo=$(CDPATH= cd -- "$here/.." && pwd)
target="$repo/hadwiger_nelson_heule_fresh_exchange_cover"
union="$repo/hadwiger_nelson_parts509_heule_union_minimum/union_510.json"
fresh="$repo/hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json"
work=$(mktemp -d /tmp/hn-heule-fresh-review.XXXXXX)
trap 'rm -rf "$work"' EXIT HUP INT TERM

python3 -B "$here/independent_check.py" \
  --union "$union" --fresh "$fresh" \
  --certificate "$target/certificate.json" \
  --target-expected "$target/expected.json" > "$work/normal.json"
cmp "$here/EXPECTED.json" "$work/normal.json"

python3 -B -O "$here/independent_check.py" \
  --union "$union" --fresh "$fresh" \
  --certificate "$target/certificate.json" \
  --target-expected "$target/expected.json" > "$work/optimized.json"
cmp "$here/EXPECTED.json" "$work/optimized.json"

sha256sum -c "$here/SHA256SUMS"
echo PASS
