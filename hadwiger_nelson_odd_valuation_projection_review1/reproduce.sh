#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo=$(CDPATH= cd -- "$here/.." && pwd)
target="$repo/hadwiger_nelson_odd_valuation_projection"
arithmetic="$repo/hadwiger_nelson_independent_moser_sum_collisions_review1/independent_audit.py"
points="$repo/hadwiger_nelson_nonmono159_214_lowden2/points159.tsv"
work=$(mktemp -d /tmp/hn-odd-projection-review.XXXXXX)
trap 'rm -rf "$work"' EXIT HUP INT TERM

python3 -B "$here/independent_check.py" \
  --arithmetic "$arithmetic" --points "$points" \
  --target-expected "$target/expected.json" > "$work/actual.json"
cmp "$here/EXPECTED.json" "$work/actual.json"

python3 -B -O "$here/independent_check.py" \
  --arithmetic "$arithmetic" --points "$points" \
  --target-expected "$target/expected.json" > "$work/actual-optimized.json"
cmp "$here/EXPECTED.json" "$work/actual-optimized.json"
sha256sum -c "$here/SHA256SUMS"
echo PASS
